from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Sum, Q, QuerySet
from django.utils.translation import gettext_lazy as _
from django_filters import FilterSet, filters


class CocktailFilterSet(FilterSet):
    search = filters.CharFilter(
        method='filter_search',
        help_text=_('Search for cocktails by name, categories and ingredients')
    )

    @staticmethod
    def filter_search(queryset: QuerySet, _, value: str):
        name_vector = SearchVector('name', weight='A')
        category_vector = SearchVector('categories__name', weight='B')
        ingredient_vector = SearchVector('composition__ingredient__name', weight='B')

        name_query = SearchQuery(value)
        category_query = SearchQuery(value)
        ingredient_separator = '+'
        if value.find(ingredient_separator) != -1:
            ingredients = ['&'.join(ingredient.split()) for ingredient in value.split(ingredient_separator)]
        else:
            ingredients = value.split()
        ingredient_query = SearchQuery('|'.join(ingredients), search_type='raw')

        return queryset.filter(
            Q(name__search=name_query)
            | Q(composition__ingredient__name__search=ingredient_query)
            | Q(categories__name__search=category_query)
        ).annotate(
            rank=(
                SearchRank(name_vector, name_query, normalization=2, cover_density=True)
                + Sum(SearchRank(category_vector, category_query, normalization=2))
                + Sum(SearchRank(ingredient_vector, ingredient_query, normalization=2))
            )
        ).order_by('-rank', 'id')
