import logging
import re

from datetime import timedelta

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db import IntegrityError, connection
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView, CreateView

from shakeit.settings import MEDIA_URL
from .forms import AddCocktailForm, UserRegisterForm, SearchForm
from .settings import COCKTAIL_RU_INPUT, RUS, COCKTAIL_EN_INPUT, ENG, COCKTAIL_ANNO, RUS_ALL, \
    COCKTAIL_MAKING, RUSENG_ALL, INGREDIENTS_LIMIT, ENG_ALL, PAGE_LIMIT, PATTERNS
from .models import DCocktailGroups, DIngredientsGroups, DUnits, TIngredients, TCocktail, \
    TCocktailIngredients, LViews, LLikes

search_form = SearchForm()
logger = logging.getLogger(__name__)
cocktail_groups = DCocktailGroups.objects.all().order_by('dcg_order')
ingredients_groups = DIngredientsGroups.objects.all().order_by('di_order')


class IndexView(TemplateView):
    template_name = 'shakeitapp/IndexView.html'
    SLIDES = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delta_week = [timezone.now() - timedelta(days=7), timezone.now()]
        delta_month = [timezone.now() - timedelta(days=30), timezone.now()]
        delta_year = [timezone.now() - timedelta(days=365), timezone.now()]
        top_week = LViews.objects \
            .select_related('lv_cocktail') \
            .filter(Q(lv_date__range=delta_week)) \
            .order_by('-lv_quantity')[:self.SLIDES]
        top_month = LViews.objects \
            .select_related('lv_cocktail') \
            .filter(Q(lv_date__range=delta_month)) \
            .order_by('-lv_quantity')[:self.SLIDES]
        top_year = LViews.objects \
            .select_related('lv_cocktail') \
            .filter(Q(lv_date__range=delta_year)) \
            .order_by('-lv_quantity')[:self.SLIDES]
        trends = [
            {
                'index': 'w',
                'name': 'Тренды недели',
                'radio': 'checked',
                'top': top_week,
            },
            {
                'index': 'm',
                'name': 'Тренды месяца',
                'radio': '',
                'top': top_month,
            },
            {
                'index': 'y',
                'name': 'Тренды года',
                'radio': '',
                'top': top_year,
            },
        ]
        slides = []
        for i in range(self.SLIDES):
            slides.append(
                {
                    'index': str(i),
                    'next': str(i + 1),
                    'prev': str(i - 1),
                    'radio': '',
                }
            )
        slides[0]['radio'] = 'checked'
        slides[-1]['next'] = '0'
        slides[0]['prev'] = str(self.SLIDES - 1)
        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title='Shakeit.su',
            subtitle='Коктейли для ваших вечеринок',
            search_form=search_form,
            top_week=top_week,
            slides=slides,
            trends=trends,
        )
        return context


class CocktailsGroupsView(TemplateView):
    """
    Класс представления типов коктейлей.
    Только GET.
    """
    template_name = 'shakeitapp/CocktailsGroupsView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title='Коктейли',
            subtitle='Виды коктейлей',
            search_form=search_form,
        )
        return context


class IngredientsGroupView(TemplateView):
    """
    Класс представления групп ингредиентов.
    Только GET.
    """
    template_name = 'shakeitapp/IngredientsGroupView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title='Ингредиенты',
            subtitle='Виды ингредиентов',
            search_form=search_form,
        )
        return context


class AddRecipeView(LoginRequiredMixin, TemplateView):
    """
    Класс представления формы добавления новых рецептов коктейлей.
    Только для зарегистрированных пользователей.
    GET и POST. При успешном добавлении коктейля производится редирект
    на его страницу.
    """
    template_name = 'shakeitapp/AddRecipeView.html'
    login_url = '/login/'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title='Добавить рецепт',
            subtitle='Создать собственный рецепт коктейля',
            form=AddCocktailForm(),
            search_form=search_form,
            RUS=RUS,
            RUS_ALL=RUS_ALL,
            ENG=ENG,
            ENG_ALL=ENG_ALL,
            RUSENG_ALL=RUSENG_ALL,
            COCKTAIL_RU_INPUT=COCKTAIL_RU_INPUT,
            COCKTAIL_EN_INPUT=COCKTAIL_EN_INPUT,
            COCKTAIL_ANNO=COCKTAIL_ANNO,
            COCKTAIL_MAKING=COCKTAIL_MAKING,
            INGREDIENTS_LIMIT=INGREDIENTS_LIMIT,
        )
        return context

    def post(self, request):
        form = AddCocktailForm(request.POST, request.FILES)
        context = self.get_context_data()
        if not form.is_valid():
            context.update(
                form=form,
                message='При загрузке произошли ошибки.',
            )
            for error in form.errors.items():
                context['message'] += '\n' + str(error)
            return render(request, self.template_name, context=context)

        cocktail_name = form.cleaned_data['cocktail_name']
        cocktail_name_translit = form.cleaned_data['cocktail_name_translit']
        cocktail_anno = form.cleaned_data['cocktail_anno']
        cocktail_making = form.cleaned_data['cocktail_making']
        cocktail_group = form.cleaned_data['cocktail_group']
        cocktail_image = form.cleaned_data['cocktail_image']
        cocktail_group = DCocktailGroups.objects.get(dcg_url=cocktail_group)

        cocktail = TCocktail(
            cocktail_name=cocktail_name,
            cocktail_name_translit=cocktail_name_translit,
            cocktail_anno=cocktail_anno,
            cocktail_making=cocktail_making,
            cocktail_image=cocktail_image,
            cocktail_author=self.request.user,
            cocktail_group=cocktail_group,
        )
        cocktail_version, postfix_ru, postfix_en = 1, '', ''
        while not cocktail.id:
            try:
                cocktail.save()
            except IntegrityError:
                cocktail_version += 1
                cocktail.cocktail_name = cocktail_name + f' вар. {cocktail_version}'
                if cocktail.cocktail_name_translit:
                    cocktail.cocktail_name_translit = cocktail_name_translit + \
                                                      f' ver. {cocktail_version}'

        # Считаем заполненные поля ингредиентов. Дальше работать будем только с ними
        i = 0
        while form.cleaned_data[f'ingredient_input_{i}']:
            ingredient_name = form.cleaned_data[f'ingredient_input_{i}']
            ingredient_value = form.cleaned_data[f'ingredient_value_{i}']
            ingredient_unit_name = form.cleaned_data[f'ingredient_unit_{i}']
            ingredient_group_url = form.cleaned_data[f'ingredient_group_{i}']
            i += 1

            ingredient_unit = DUnits.objects.get(du_name=ingredient_unit_name)
            ingredient_group = DIngredientsGroups.objects.get(di_url=ingredient_group_url)

            ingredient = TIngredients.objects.filter(ingredient_name=ingredient_name).first()
            if not ingredient:
                ingredient = TIngredients(
                    ingredient_name=ingredient_name,
                    ingredient_group=ingredient_group,
                )
                ingredient.save()
            cocktail_ingredients = TCocktailIngredients(
                ci_cocktail=cocktail,
                ci_ingredient=ingredient,
                ci_unit=ingredient_unit,
                ci_quantity=ingredient_value,
            )
            cocktail_ingredients.save()

        cocktail.cocktail_image.delete(save=True)
        cocktail_image = form.cleaned_data['cocktail_image']
        file_extension = cocktail_image.name.split('.')[-1]
        cocktail_image.name = f'cocktail_{cocktail.cocktail_url}.{file_extension}'
        cocktail.cocktail_image = cocktail_image
        cocktail.save()
        return redirect(f'/cocktail/{cocktail.cocktail_url}/', permanent=True)


class CocktailView(TemplateView):
    """
    Класс представления страницы коктейля.
    Только GET.
    """
    template_name = 'shakeitapp/CocktailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url = kwargs.get('url')
        active_user = self.request.user.is_authenticated
        # Ей-богу, проще и понятнее на SQL написать запросы
        cocktail = TCocktail.objects \
            .select_related('cocktail_group') \
            .select_related('cocktail_author') \
            .filter(cocktail_url=url) \
            .first()
        cocktail_ingredients = TCocktailIngredients.objects \
            .select_related('ci_ingredient') \
            .select_related('ci_unit') \
            .filter(ci_cocktail=cocktail) \
            .order_by('id')
        like = False
        try:
            like = LLikes.objects \
                .filter(ll_cocktail=cocktail, ll_user=self.request.user) \
                .first() \
                .ll_is_like
        except (AttributeError, TypeError):
            pass

        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title=cocktail.cocktail_name,
            subtitle='Рецепт коктейля',
            search_form=search_form,
            cocktail=cocktail,
            cocktail_ingredients=cocktail_ingredients,
            active_user=active_user,
            like=like,
        )

        current_date = timezone.now().date()
        view_counter = LViews.objects.filter(
            lv_cocktail=cocktail, lv_date=current_date
        ).first()
        if view_counter:
            view_counter.lv_quantity += 1
            view_counter.save()
        else:
            view_counter = LViews(
                lv_date=current_date,
                lv_quantity=1,
                lv_cocktail=cocktail,
            )
            view_counter.save()

        return context


class AllCocktailsView(TemplateView):
    """
    Класс представления страниц с коктейлями.
    Только GET.
    """
    template_name = 'shakeitapp/AllCocktailsView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = kwargs.get('page', 1)
        group = kwargs.get('group')
        max_pages = TCocktail.objects.count() // PAGE_LIMIT
        left_slice = page * PAGE_LIMIT - PAGE_LIMIT
        right_slice = page * PAGE_LIMIT
        cocktails = TCocktail.objects \
            .select_related('cocktail_group') \
            .select_related('cocktail_author') \
            .filter(cocktail_group__dcg_url=group) \
            .order_by('id')[left_slice:right_slice]
        group = DCocktailGroups.objects.get(dcg_url=group)
        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title='Поиск рецепта',
            subtitle=f'Выбор коктейля по типу: {group.dcg_name}',
            search_form=search_form,
            cocktails=cocktails,
            previous=page - 1 if page > 1 else None,
            next=page + 1 if page < max_pages else None,
            group_url=group.dcg_url,
        )
        return context


class RegisterUserView(CreateView):
    """
    Класс представления страницы регистрации пользователя.
    Стандартная форма регистрации Django.
    """
    form_class = UserRegisterForm
    template_name = 'shakeitapp/RegisterUserView.html'
    success_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title='Регистрация',
            subtitle='Регистрация нового пользователя на сайте',
        )
        return context


class LoginUserView(LoginView):
    """
    Класс представления формы входа пользователя на сайт.
    Стандартная форма Django.
    """
    form_class = AuthenticationForm
    template_name = 'shakeitapp/LoginUserView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title='Войти',
            subtitle='Вход на сайт под своей учетной записью',
        )
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'shakeitapp/HomeView.html'
    login_url = '/login/'
    redirect_field_name = "redirect_to"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        user = User.objects.get(id=user_id)
        cocktail_likes = LLikes.objects. \
            select_related('ll_user'). \
            select_related('ll_cocktail'). \
            filter(ll_is_like=True). \
            order_by('ll_cocktail_id__cocktail_name')
        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title='Профиль',
            subtitle='Редактирование профиля пользователя',
            search_form=search_form,
            user_name=user.username,
            cocktail_likes=cocktail_likes,
        )
        return context


class IngredientsInGroupView(TemplateView):
    """
    Класс представления страницы с ингредиентами
    """
    template_name = 'shakeitapp/IngredientsInGroupView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_url = kwargs.get('group')
        # Что за фигня с LEFT JOIN у Django ORM?!
        # Изображения придется реализовывать через
        # кастомные фильтры и дополнительные запросы к СУБД.
        # Всего один LEFT JOIN! Sic!
        ingredients = TIngredients.objects \
            .select_related('ingredient_group') \
            .filter(ingredient_group__di_url=group_url) \
            .order_by('ingredient_name')
        group_name = DIngredientsGroups.objects \
            .filter(di_url=group_url) \
            .first() \
            .di_name
        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title='Поиск рецепта',
            subtitle=f'Выбор коктейля по виду ингредиента: {group_name}',
            search_form=search_form,
            ingredients=ingredients,
        )
        return context


class IngredientsInCocktailsView(TemplateView):
    """
    Класс представления страницы выбора коктейля по ингредиенту
    """
    template_name = 'shakeitapp/IngredientsInCocktailsView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = kwargs.get('page', 1)
        ingredient_url = kwargs.get('ingredient')
        max_pages = TCocktail.objects.count() // PAGE_LIMIT
        left_slice = page * PAGE_LIMIT - PAGE_LIMIT
        right_slice = page * PAGE_LIMIT
        cocktails_by_ingredient = TCocktailIngredients.objects \
            .select_related('ci_cocktail') \
            .select_related('ci_ingredient') \
            .filter(ci_ingredient__ingredient_url=ingredient_url) \
            .order_by('ci_cocktail_id__cocktail_name')[left_slice: right_slice]
        ingredient = TIngredients.objects \
            .filter(ingredient_url=ingredient_url).first()
        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title='Поиск рецепта',
            subtitle=f'Выбор коктейля по ингредиенту:{ingredient.ingredient_name}',
            search_form=search_form,
            cocktails_by_ingredient=cocktails_by_ingredient,
            ingredient_url=ingredient_url,
            previous=page - 1 if page > 1 else None,
            next=page + 1 if page < max_pages else None,
        )
        return context


class SearchView(TemplateView):
    """
    Класс представления страницы поиска
    """
    template_name = 'shakeitapp/SearchView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_string = self.request.GET.get('q', None)
        page = self.request.GET.get('p')
        try:
            page = int(page)
        except (ValueError, TypeError):
            page = 1
        previous_page = page - 1
        if previous_page < 1:
            previous_page = None
        next_page = None
        left_slice = page * PAGE_LIMIT - PAGE_LIMIT
        view_search_form = search_form
        cocktails = None
        if search_string:
            search_string = re.sub(PATTERNS[RUSENG_ALL], '', search_string)
            view_search_form = SearchForm(
                initial={
                    'q': search_string,
                }
            )
            search_words = search_string.split()
            q = f'''
            SELECT
                tc.cocktail_name as cocktail_name,
                tc.cocktail_url as cocktail_url,
                tc.cocktail_anno as cocktail_anno,
                tc.cocktail_image as cocktail_image,
                au.username as username
            FROM
                shakeitapp_tcocktail AS tc
            LEFT JOIN
                shakeitapp_tcocktailingredients as tci
            ON
                tc.id = tci.ci_cocktail_id
            LEFT JOIN
                shakeitapp_tingredients as ti
            ON
                tci.ci_ingredient_id = ti.id
            LEFT JOIN
                auth_user as au
            ON
                tc.cocktail_author_id = au.id
            WHERE
                ({
            ' AND '.join([
                f"(tc.cocktail_name LIKE '%{word}%'"
                "    OR"
                f" tc.cocktail_anno LIKE '%{word}%'"
                "    OR"
                f" tc.cocktail_making LIKE '%{word}%'"
                "    OR"
                f" ti.ingredient_name LIKE '%{word}%')"
                for word in search_words
            ])
            })
            GROUP BY
                tc.cocktail_name,
                tc.cocktail_url,
                tc.cocktail_anno,
                tc.cocktail_image,
                au.username
            ORDER BY
                tc.id
            LIMIT {left_slice}, {PAGE_LIMIT + 1};
            '''
            with connection.cursor() as cursor:
                cursor.execute(q)
                cocktails = cursor.fetchall()
            cocktails = [list(cocktail) for cocktail in cocktails]
            for i in range(len(cocktails)):
                cocktails[i][3] = f'{MEDIA_URL}{cocktails[i][3]}'
            if len(cocktails) > PAGE_LIMIT:
                next_page = page + 1
                cocktails = cocktails[:PAGE_LIMIT]
        context.update(
            cocktail_groups=cocktail_groups,
            ingredients_groups=ingredients_groups,
            title='Поиск рецепта',
            subtitle=f'Найди свой коктейль',
            search_form=view_search_form,
            cocktails=cocktails,
            search_string=search_string,
            previous=previous_page,
            next=next_page,
        )
        return context
