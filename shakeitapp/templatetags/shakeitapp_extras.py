import logging

from django import template
from django.templatetags.static import static

from shakeitapp.models import TGenIngredientsImages
from shakeitapp.settings import GENERIC_INGREDIENT_IMAGE

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def get_cocktail(trend, cocktail_index):
    """
    Возвращает рецепт из топа рецептов по его индексу
    Аргументы:
        trend - набор данных по тренду
        cocktail - индекс рецепта в топе
    """
    return trend['top'][int(cocktail_index)]


@register.filter
def get_cocktail_image(cocktail):
    """
    Возвращает ссылку на изображение коктейля
    """
    return cocktail.lv_cocktail.cocktail_image.url


@register.filter
def get_cocktail_name(cocktail):
    """
    Возвращает наименование коктейля
    """
    return cocktail.lv_cocktail.cocktail_name


@register.filter
def get_cocktail_anno(cocktail):
    """
    Возвращает описание коктейля
    """
    return cocktail.lv_cocktail.cocktail_anno


@register.filter
def get_cocktail_url(cocktail):
    """
    Возвращает ссылку на коктейль
    """
    return cocktail.lv_cocktail.cocktail_url


@register.filter
def get_field(form, field_name):
    """
    Принимает экземпляр Form и имя поля. Возвращаемое значение будет
    использоваться при доступе к полю в шаблоне.
    """
    return form.fields[field_name].get_bound_field(form, field_name)


@register.filter
def make_counter(top_limit) -> list:
    """
    Создает список значений от 0 до заданного предела для цикла for в шаблоне.
    Аргументы:
        top_limit - верхний предел списка значений (не включается в список)
    """
    return [str(value) for value in range(int(top_limit))]


@register.filter
def get_ingredient_img(ingredient_url):
    """
    Возвращает последнюю по дате одобренную ссылку на изображение ингредиенте из таблицы
    изображений Кандинского, если она там есть, или ссылку на generic-изображение
    """
    image = TGenIngredientsImages.objects \
        .select_related('gi_ingredient') \
        .filter(gi_status=TGenIngredientsImages.ImageStatus.APPROVED) \
        .filter(gi_ingredient__ingredient_url=ingredient_url) \
        .order_by('-gi_date_done') \
        .first()
    if image:
        return image.gi_image.url
    return static(GENERIC_INGREDIENT_IMAGE)
