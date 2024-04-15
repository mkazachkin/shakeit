from django.contrib.auth.views import LogoutView
from django.views.generic.base import RedirectView
from django.urls import path
from .views import IndexView, CocktailsGroupsView, IngredientsGroupView, AddRecipeView, RegisterUserView, LoginUserView, \
    HomeView, AllCocktailsView, CocktailView, IngredientsInGroupView, IngredientsInCocktailsView, SearchView

urlpatterns = [
    path('', IndexView.as_view(), name='Index'),
    path('cocktail/', RedirectView.as_view(url='/cocktails/')), 
    path('cocktails/', CocktailsGroupsView.as_view(), name='Cocktails'),
    path('ingredients/', IngredientsGroupView.as_view(), name='Ingredients'),
    path('ingredients/<str:group>/', IngredientsInGroupView.as_view(), name='Ingredients in group'),
    path('ingredients/<str:group>/<str:ingredient>/', IngredientsInCocktailsView.as_view(),
         name='Ingredients in cocktails'),
    path('add/', AddRecipeView.as_view(), name='Add cocktails'),
    path('register/', RegisterUserView.as_view(), name='Register user'),
    path('login/', LoginUserView.as_view(), name='Login user'),
    path('logout/', LogoutView.as_view(), name='Logout user'),
    path('home/', HomeView.as_view(), name='Users home'),
    path('cocktails/<str:group>/', AllCocktailsView.as_view(), name='Cocktails list'),
    path('cocktails/<str:group>/<int:page>/', AllCocktailsView.as_view(), name='Cocktails pages'),
    path('cocktail/<str:url>/', CocktailView.as_view(), name='Cocktail recipe'),
    path('search/', SearchView.as_view(), name='Search recipe'),
]
