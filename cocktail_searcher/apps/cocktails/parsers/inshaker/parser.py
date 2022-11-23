import asyncio
import logging
import unicodedata
from dataclasses import dataclass
from typing import Union, List
from urllib.parse import urljoin

import httpx
import lxml.html
from django.db import transaction

from apps.cocktails import models
from cocktail_searcher import settings


@dataclass
class Composition:
    """Состав коктейля"""
    ingredient_name: str
    amount: int
    unit: str


@dataclass
class Cocktail:
    name: str
    image_url: str
    categories: List[str]
    composition: List[Composition]
    recipe: List[str]


logger = logging.getLogger(__name__)


class InshakerParser:
    """Парсер Inshaker"""

    def run(self):
        logger.info('Cocktail parsing started...')

        logger.info('Get urls to cocktail pages')
        urls = self._get_cocktail_urls()
        url_block_size = 20
        urls = [urls[i:i+url_block_size] for i in range(0, len(urls), url_block_size)]

        loop = asyncio.get_event_loop()
        client = httpx.AsyncClient()
        for url_block in urls:
            logger.info(f'Get cocktail pages {url_block}')
            tasks = [self._fetch(client, url) for url in url_block]
            htmls = loop.run_until_complete(asyncio.gather(*tasks))
            cocktails = []
            for html in htmls:
                try:
                    cocktails.append(self._scraping_cocktail_info(html))
                except IndexError:
                    logger.error('Cocktail information scrapping error', exc_info=True)

            logger.info('Saving cocktails to the database...')
            for cocktail in cocktails:
                db_cocktail = models.Cocktail.objects.filter(name=cocktail.name).first()
                if not db_cocktail:
                    self._save_cocktail(cocktail)
                else:
                    logger.info(f'Cocktail "{cocktail.name}" already exists. Save skip.')

        loop.run_until_complete(client.aclose())
        logger.info('Parsing done!')

    def _get_cocktail_urls(self) -> List[str]:
        """Получает ссылки на страницы коктейлей"""
        response = httpx.get(
            url=urljoin(settings.INSHAKER_BASE_URL, settings.INSHAKER_COCKTAILS_PATH),
            params={'random_page': 1000}
        )

        doc = self._parse_html(response.text)
        urls = doc.xpath(settings.INSHAKER_COCKTAIL_URLS_XPATH)
        urls = [urljoin(settings.INSHAKER_BASE_URL, url) for url in urls]

        return urls

    def _scraping_cocktail_info(self, html_source: Union[bytes, str]) -> Cocktail:
        """Извлекает данные о коктейле со страницы коктейля

        Args:
            html_source: исходных код страницы коктейля

        Returns:
            Экземпляр класса `Cocktail`, содержащий информацию о коктейле

        Raises:
            IndexError: возбуждаемое исключение в случае ошибки извлечения данных о коктейле
        """
        doc = self._parse_html(html_source)

        name = self._normalize_text(doc.xpath(settings.INSHAKER_COCKTAIL_NAME_XPATH)[0])
        image_url = urljoin(settings.INSHAKER_BASE_URL, doc.xpath(settings.INSHAKER_COCKTAIL_IMAGE_XPATH)[0])
        categories = [self._normalize_text(category.capitalize())
                      for category in doc.xpath(settings.INSHAKER_COCKTAIL_CATEGORIES_XPATH)]

        ingredients = doc.xpath(settings.INSHAKER_COCKTAIL_INGREDIENTS_XPATH)
        composition = []
        for ingredient in ingredients:
            ingredient_name = self._normalize_text(
                ingredient.xpath(settings.INSHAKER_INGREDIENT_NAME_XPATH)[0].rstrip()
            )
            amount = ingredient.xpath(settings.INSHAKER_INGREDIENT_AMOUNT_XPATH)[0]
            unit = self._normalize_text(ingredient.xpath(settings.INSHAKER_INGREDIENT_UNIT_XPATH)[0])
            composition.append(Composition(ingredient_name, amount, unit))

        recipe = [self._normalize_text(stage) for stage in doc.xpath(settings.INSHAKER_COCKTAIL_RECIPE_XPATH)]

        return Cocktail(name, image_url, categories, composition, recipe)

    @staticmethod
    @transaction.atomic
    def _save_cocktail(cocktail: Cocktail):
        """Сохраняет коктейль в базу данных

        Args:
            cocktail: DTO коктейля
        """
        db_cocktail = models.Cocktail.objects.create(name=cocktail.name, image_url=cocktail.image_url)

        db_cocktail.categories.set(
            [models.Category.objects.get_or_create(name=category)[0] for category in cocktail.categories]
        )

        db_composition = []
        for composition in cocktail.composition:
            db_ingredient = models.Ingredient.objects.get_or_create(name=composition.ingredient_name)[0]
            db_unit = models.Unit.objects.get_or_create(name=composition.unit)[0]
            db_composition.append(
                models.Composition(
                    cocktail=db_cocktail,
                    ingredient=db_ingredient,
                    amount=composition.amount,
                    unit=db_unit)
            )
        models.Composition.objects.bulk_create(db_composition)

        recipe = [models.Recipe(cocktail=db_cocktail, stage=stage, action=action)
                  for stage, action in enumerate(cocktail.recipe, start=1)]
        models.Recipe.objects.bulk_create(recipe)

    @staticmethod
    async def _fetch(client: httpx.AsyncClient, url: str) -> str:
        response = await client.get(url)

        return response.text

    @staticmethod
    def _parse_html(html_source: Union[bytes, str]) -> lxml.html.HtmlElement:
        return lxml.html.fromstring(html_source)

    @staticmethod
    def _normalize_text(string: str) -> str:
        """Нормализует строку `string` к нормальной форме NFKC

        Args:
            string: нормализируемая строка

        Returns:
            Нормализованная строка формы NFKC
        """
        return string if unicodedata.is_normalized('NFKC', string) else unicodedata.normalize('NFKC', string)
