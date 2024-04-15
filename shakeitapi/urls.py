from django.urls import path
from .views import DUnitsAPIView, DIngredientsGroupsAPIView, DCocktailGroupsAPIView, LLikesAPIView

urlpatterns = [
    path('get_units/', DUnitsAPIView.as_view(), name='Units API'),
    path('get_ingredients_groups/', DIngredientsGroupsAPIView.as_view(), name='Ingredients Groups API'),
    path('get_cocktail_groups/', DCocktailGroupsAPIView.as_view(), name='Cocktails Groups API'),
    path('post_like/', LLikesAPIView.as_view(), name='Likes API'),
]
