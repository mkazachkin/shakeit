import logging

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .abstract.model import ModelWTruncate
from .utils.tools import ru_string_translit


logger = logging.getLogger(__name__)


class DCocktailGroups(ModelWTruncate):
    """
    Словарь видов коктейлей. Содержит:
        Название вида коктейлей на русском языке
        Название вида в транслитерации или перевод на английский язык
        URL
        Описание вида коктейлей
        Порядок вывода
    """
    class Meta:
        verbose_name = 'Вид коктейля'
        verbose_name_plural = 'Виды коктейлей'

    dcg_name = models.CharField(
        max_length=128,
        null=False,
        unique=True,
        verbose_name='Наименование вида коктейля',
    )
    dcg_name_translit = models.CharField(
        max_length=128,
        db_index=True,
        unique=True,
        verbose_name='Транслитерация наименования',
    )
    dcg_url = models.CharField(
        max_length=128,
        db_index=True,
        unique=True,
        verbose_name='Ссылочное представление наименования',
    )
    dcg_anno = models.TextField(
        null=False,
        verbose_name='Описание вида',
    )
    dcg_order = models.IntegerField(
        null=False,
        verbose_name='Порядок вывода в меню',
    )

    def __str__(self):
        return f'{self.dcg_name} коктейли'

    def save(self, *args, **kwargs):
        """
        Автоматически генерирует транслитерацию, URL и сохраняет ее в БД
        """
        if not self.dcg_name_translit or self.dcg_name_translit == '':
            self.dcg_name_translit = ru_string_translit(str(self.dcg_name))
        self.dcg_url = slugify(self.dcg_name_translit)

        if not self.dcg_order:
            dcg_order_max = DCocktailGroups.objects.aggregate(Max('dcg_order'))['dcg_order__max']
            if not dcg_order_max:
                dcg_order_max = 0
            self.dcg_order = dcg_order_max + 1

        super().save(*args, **kwargs)


class DIngredientsGroups(ModelWTruncate):
    """
    Словарь видов ингредиентов. Содержит:
        Название вида ингредиента на русском языке
        Название вида в транслитерации или перевод на английский язык
        Описание вида ингредиента
        Порядок вывода
    """
    class Meta:
        verbose_name = 'Вид ингредиента'
        verbose_name_plural = 'Виды ингредиентов'

    di_name = models.CharField(
        max_length=128,
        null=False,
        unique=True,
        verbose_name='Наименование вида ингредиента',
    )
    di_name_translit = models.CharField(
        max_length=128,
        db_index=True,
        unique=True,
        verbose_name='Транслитерация наименования',
    )
    di_url = models.CharField(
        max_length=128,
        db_index=True,
        unique=True,
        verbose_name='Ссылочное представление наименования',
    )
    di_anno = models.TextField(
        null=False,
        verbose_name='Описание вида',
    )
    di_order = models.IntegerField(
        null=False,
        verbose_name='Порядок вывода в меню'
    )

    def __str__(self):
        return f'{self.di_name} для коктейлей'

    def save(self, *args, **kwargs):
        """
        Автоматически генерирует транслитерацию, URL и сохраняет ее в БД
        """
        if not self.di_name_translit or self.di_name_translit == '':
            self.di_name_translit = ru_string_translit(str(self.di_name))
        self.di_url = slugify(self.di_name_translit)

        if not self.di_order:
            di_order_max = DIngredientsGroups.objects.aggregate(Max('di_order'))['di_order__max']
            if not di_order_max:
                di_order_max = 0
            self.di_order = di_order_max + 1

        super().save(*args, **kwargs)


class DUnits(ModelWTruncate):
    """
    Словарь единиц измерения. Содержит:
        Краткое написание единицы измерения (мл, мг и т. п.) на русском языке
        Полное описание единицы измерения
    """
    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'

    du_name = models.CharField(
        max_length=16,
        null=False,
        db_index=True,
        unique=True,
        verbose_name='Обозначение единицы измерения',
    )
    du_anno = models.CharField(
        max_length=128,
        null=False,
        verbose_name='Краткое описание',
    )

    def __str__(self):
        return f'{self.du_anno} ({self.du_name})'


class TCocktail(ModelWTruncate):
    """
    Таблица коктейлей. Содержит:
        Название коктейля на русском языке
        Название коктейля в транслитерации или перевод на английский язык
        Идентификатор вида коктейля
        Идентификатор пользователя, добавившего коктейль в БД
        Описание коктейля
        Название файла с изображением коктейля
        Описание процесса приготовления коктейля
    """
    class Meta:
        verbose_name = 'Коктейль'
        verbose_name_plural = 'Коктейли'

    cocktail_name = models.CharField(
        max_length=128,
        null=False,
        unique=True,
        verbose_name='Наименование коктейля',
    )
    cocktail_name_translit = models.CharField(
        max_length=128,
        db_index=True,
        unique=True,
        verbose_name='Транслитерация наименования',
    )
    cocktail_url = models.CharField(
        max_length=128,
        db_index=True,
        unique=True,
        verbose_name='Ссылочное представление наименования',
    )
    cocktail_group = models.ForeignKey(
        DCocktailGroups,
        on_delete=models.CASCADE,
        verbose_name='Вид коктейля по словарю',
    )
    cocktail_author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    cocktail_anno = models.CharField(
        max_length=1024,
        null=False,
        verbose_name='Описание коктейля',
    )
    cocktail_making = models.CharField(
        max_length=1024,
        null=False,
        verbose_name='Описание процесса приготовления',
    )
    cocktail_image = models.ImageField(
        null=False,
        default='cocktail_generic.jpg',
        verbose_name='Изображение коктейля',
    )

    def __str__(self):
        return self.cocktail_name

    def save(self, *args, **kwargs):
        """
        Автоматически генерирует транслитерацию, URL и сохраняет ее в БД
        """
        if not self.cocktail_name_translit or self.cocktail_name_translit == '':
            self.cocktail_name_translit = ru_string_translit(str(self.cocktail_name))

        self.cocktail_url = slugify(self.cocktail_name_translit)

        super().save(*args, **kwargs)


class TIngredients(ModelWTruncate):
    """
    Таблица ингредиентов коктейлей. Содержит:
        Название ингредиента
        Название ингредиента в транслитерации или перевод на английский язык
        Идентификатор вида ингредиента
    """
    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    ingredient_name = models.CharField(
        max_length=128,
        db_index=True,
        unique=True,
        verbose_name='Наименование ингредиента',
    )
    ingredient_name_translit = models.CharField(
        max_length=128,
        db_index=True,
        unique=True,
        verbose_name='Транслитерация наименования',
    )
    ingredient_group = models.ForeignKey(
        DIngredientsGroups,
        on_delete=models.CASCADE,
        verbose_name='Вид ингредиента по словарю'
    )
    ingredient_url = models.CharField(
        max_length=128,
        db_index=True,
        unique=True,
        verbose_name='Ссылочное представление наименования'
    )

    def __str__(self):
        return self.ingredient_name

    def save(self, *args, **kwargs):
        """
        Автоматически генерирует транслитерацию, URL и сохраняет ее в БД
        """
        if not self.ingredient_name_translit or self.ingredient_name_translit == '':
            self.ingredient_name_translit = ru_string_translit(str(self.ingredient_name))

        self.ingredient_url = slugify(self.ingredient_name_translit)

        super().save(*args, **kwargs)


class TCocktailIngredients(ModelWTruncate):
    """
    Таблица ингредиентов коктейлей. Содержит:
        Идентификатор коктейля
        Идентификатор ингредиента
        Идентификатор единицы измерения
        Количество ингредиента (допускается свободное описания количества, например "по-вкусу"
    """
    class Meta:
        verbose_name = 'Ингредиент коктейля'
        verbose_name_plural = 'Ингредиенты коктейлей'

    ci_cocktail = models.ForeignKey(
        TCocktail,
        on_delete=models.CASCADE,
        verbose_name='Коктейль',
    )
    ci_ingredient = models.ForeignKey(
        TIngredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    ci_unit = models.ForeignKey(
        DUnits,
        on_delete=models.CASCADE,
        verbose_name='Единица измерения',
    )
    ci_quantity = models.CharField(
        max_length=64,
        null=False,
        verbose_name='Количество',
    )

    def __str__(self):
        cocktail = TCocktail.objects \
            .filter(id=self.ci_cocktail.id) \
            .first()
        ingredient = TIngredients.objects \
            .filter(id=self.ci_ingredient.id) \
            .first()
        return f'{ingredient.ingredient_name} для коктейля '\
               f'"{cocktail.cocktail_name}"'


class LLikes(ModelWTruncate):
    """
    Таблица лайков пользователей. Содержит:
        Идентификатор пользователя
        Идентификатор коктейля
        Дата лайка
    """
    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

    ll_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name='Пользователь',
    )
    ll_cocktail = models.ForeignKey(
        TCocktail,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name='Коктейль',
    )
    ll_is_like = models.BooleanField(
        db_index=True,
        verbose_name='Лайк',
    )

    def __str__(self):
        if self.ll_is_like:
            return 'Лайк'
        return 'Дизлайк'


class LViews(ModelWTruncate):
    """
    Таблица просмотра страниц коктейлей. Содержит:
        Идентификатор коктейля
        Дата просмотров
        Количество просмотров
    """
    class Meta:
        verbose_name = 'Просмотры'
        verbose_name_plural = 'Просмотры'

    lv_cocktail = models.ForeignKey(
        TCocktail,
        on_delete=models.CASCADE,
        verbose_name='Коктейль',
    )
    lv_date = models.DateField(
        null=False,
        db_index=True,
        verbose_name='Дата просмотров',
    )
    lv_quantity = models.BigIntegerField(
        null=False,
        db_index=True,
        verbose_name='Количество просмотров',
    )

    def __str__(self):
        cocktail = TCocktail.objects \
            .filter(id=self.lv_cocktail.id) \
            .first()
        return f'П осмотры {cocktail.cicktail_name} за {self.lv_date}'


class TGenIngredientsImages(ModelWTruncate):
    """
    Таблица списка ингредиентов на генерацию изображения нейросетью. Содержит:
        Идентификатор ингредиента
        Дата добавления задания
        Дата выполнения задания
        Ссылка на изображение ингредиента
    """
    class Meta:
        verbose_name = 'Изображения ингредиента от Kandinsky'
        verbose_name_plural = 'Изображения ингредиентов от Kandinsky'

    class ImageStatus(models.TextChoices):
        INITIATED = 'IN', _('Инициализировано')
        GENERATED = 'GE', _('Сгенерировано')
        CENSORED = 'CE', _('Цензура')
        APPROVED = 'AP', _('Одобрено')
        DISAPPROVED = 'DI', _('Отклонено')

    gi_ingredient = models.ForeignKey(
        TIngredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    gi_date_add = models.DateTimeField(
        null=False,
        verbose_name='Дата добавления',
    )
    gi_date_done = models.DateField(
        null=True,
        verbose_name='Дата генерации изображения',
    )
    gi_status = models.CharField(
        null=False,
        max_length=2,
        choices=ImageStatus.choices,
        default=ImageStatus.INITIATED,
        verbose_name='Статус генерации',
    )
    gi_image = models.ImageField(
        null=True,
        verbose_name='Изображение ингредиента',
    )

    def __str__(self):
        ingredient = TIngredients.objects \
            .filter(id=self.gi_ingredient.id) \
            .first()
        if self.gi_status == 'DI':
            return f'Забракованное изображение {ingredient.ingredient_name}.'
        elif self.gi_status == 'AP':
            return f'Одобренное к применению изображение {ingredient.ingredient_name}.'
        elif self.gi_status == 'CE':
            return f'Изображение {ingredient.ingredient_name} не прошедшее цензуру.'
        elif self.gi_status == 'GE':
            return f'Сгенерированное изображение {ingredient.ingredient_name}.'
        return f'Изображение {ingredient.ingredient_name} добавленное на генерацию.'
