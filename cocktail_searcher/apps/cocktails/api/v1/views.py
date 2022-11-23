from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from apps.cocktails.api.v1.filtersets import CocktailFilterSet
from apps.cocktails.api.v1.serializers import CocktailSerializer, RecipeSerializer
from apps.cocktails.models import Cocktail


@extend_schema(tags=['Cocktails'])
class CocktailViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Cocktail.objects.prefetch_related(
        'categories',
        'composition',
        'composition__ingredient',
        'composition__unit',
    ).order_by('id')
    serializer_class = CocktailSerializer
    filterset_class = CocktailFilterSet

    @extend_schema(responses=RecipeSerializer(many=True),
                   filters=False,
                   summary='Get a list of cocktail "Recipe" entities')
    @action(methods=['get'], detail=True, pagination_class=None)
    def recipe(self, request, pk=None, *args, **kwargs):
        queryset = Cocktail.objects.all()
        cocktail = get_object_or_404(queryset, pk=pk)

        serializer = RecipeSerializer(cocktail.recipe.order_by('stage'), many=True)

        return Response(serializer.data)
