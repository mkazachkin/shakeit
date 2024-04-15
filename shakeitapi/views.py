from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from shakeitapp.models import DUnits, DIngredientsGroups, DCocktailGroups, LLikes
from .serializers import UnitsSerializer, IngredientsGroupsSerializer, CocktailGroupsSerializer, \
    WriterLikePostSerializer


class DUnitsAPIView(generics.ListAPIView):
    """
    Класс представления API для получения списка единиц измерения.
    Возвращает в API JSON список единиц измерения из базы данных DUnits
    """
    queryset = DUnits.objects.all()
    serializer_class = UnitsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class DIngredientsGroupsAPIView(generics.ListAPIView):
    """
    Класс представления API для получения видов ингредиентов.
    Возвращает в API JSON список единиц измерения из базы данных DIngredientsGroups.
    """
    queryset = DIngredientsGroups.objects.all()
    serializer_class = IngredientsGroupsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class DCocktailGroupsAPIView(generics.ListAPIView):
    """
    Класс представления API для получения видов коктейлей.
    Возвращает в API JSON список видов коктейлей из базы данных DIngredientsGroups.
    """
    queryset = DCocktailGroups.objects.all()
    serializer_class = CocktailGroupsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class LLikesAPIView(generics.CreateAPIView):
    queryset = LLikes.objects.all()
    serializer_class = WriterLikePostSerializer
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            request=self.request,
        )
        return context
