from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import DUnits
from .settings import COCKTAIL_RU_INPUT, RUS, COCKTAIL_EN_INPUT, ENG, COCKTAIL_ANNO, RUS_ALL, \
    COCKTAIL_MAKING, RUSENG_ALL, INGREDIENTS_LIMIT, PATTERNS


class UserRegisterForm(UserCreationForm):
    """
    Класс формы регистрации пользователя.
    Используется стандартная форма Django с именем пользователя
    и адресом электронной почты.
    """
    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }


class AddCocktailForm(forms.Form):
    """
    Класс формы добавления рецепта в базу данных.
    """
    cocktail_name = forms.CharField(
        max_length=128,
        required=True,
        label='Название коктейля на русском языке',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Название коктейля',
                'onkeyup': f'checkTextInput({COCKTAIL_RU_INPUT}, {RUS});',
                'onchange': f'checkTextInput({COCKTAIL_RU_INPUT}, {RUS});',
            }
        )
    )
    cocktail_name_translit = forms.CharField(
        max_length=128,
        required=False,
        label='Название коктейля на английском языке (необязательно)',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Cocktail name',
                'onkeyup': f'checkTextInput({COCKTAIL_EN_INPUT}, {ENG})',
                'onchange': f'checkTextInput({COCKTAIL_EN_INPUT}, {ENG})',
            }
        )
    )
    cocktail_anno = forms.CharField(
        max_length=1024,
        required=True,
        label='Описание коктейля',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Введите краткое описание коктейля на русском языке',
                'onkeyup': f'checkTextInput({COCKTAIL_ANNO}, {RUS_ALL});',
                'onchange': f'checkTextInput({COCKTAIL_ANNO}, {RUS_ALL});',
            }
        ),

    )
    cocktail_making = forms.CharField(
        max_length=1024,
        required=True,
        label='Процесс приготовления коктейля',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Введите краткое описание процесса '
                               'приготовления коктейля на русском языке',
                'onkeyup': f'checkTextInput({COCKTAIL_MAKING}, {RUSENG_ALL});',
                'onchange': f'checkTextInput({COCKTAIL_MAKING}, {RUSENG_ALL});',
            }
        )
    )

    cocktail_group = forms.CharField(
        required=True,
        max_length=128,
        widget=forms.HiddenInput(),
    )

    cocktail_image = forms.ImageField(
        label='Загрузите изображение',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы добавления рецепта в базу данных.
        Инициализируются поля ввода ингредиентов коктейлей.
        Количество полей зависит от установленной в модуле константы
        максимума INGREDIENTS_LIMIT. Паттерны проверки задаются
        словарем PATTERNS.
        """
        super(AddCocktailForm, self).__init__(*args, **kwargs)
        for i in range(INGREDIENTS_LIMIT):
            self.fields[f'ingredient_input_{i}'] = forms.CharField(
                max_length=128,
                required=False,
                widget=forms.TextInput(
                    attrs={
                        'placeholder': 'Введите название ингредиента',
                        'class': 'ingredient__input',
                        'onchange': f'checkTextInput({i}, {RUS});',
                        'onkeyup': f'checkTextInput({i}, {RUS});',
                    }
                )
            )
            self.fields[f'ingredient_value_{i}'] = forms.IntegerField(
                required=False,
                widget=forms.NumberInput(
                    attrs={
                        'class': 'ingredient__unit__input',
                        'onchange': f'checkIntInput({i})',
                        'onkeyup': f'checkIntInput({i})',
                    }
                )
            )
            # Не используется max_length, т.к это Select. HTML с max_length не проходит валидацию
            self.fields[f'ingredient_unit_{i}'] = forms.CharField(
                required=False,
                widget=forms.Select(
                    choices=(
                        (unit['du_name'], unit['du_name'])
                        for unit in DUnits.objects.values('du_name')
                    ),
                )
            )
            self.fields[f'ingredient_group_{i}'] = forms.CharField(
                required=False,
                max_length=128,
                widget=forms.HiddenInput,
            )

    def clean_cocktail_name(self):
        """
        Проверка названия коктейля на валидность.
        """
        cocktail_name = self.cleaned_data['cocktail_name']
        if PATTERNS[RUS].match(cocktail_name):
            raise forms.ValidationError(
                'В названии коктейля недопустимые символы.'
            )
        return cocktail_name

    def clean_cocktail_name_translit(self):
        """
        Проверка названия коктейля на английском языке
        """
        cocktail_name_translit = self.cleaned_data['cocktail_name_translit']
        if PATTERNS[ENG].match(cocktail_name_translit):
            raise forms.ValidationError(
                'В названии коктейля на английском языке недопустимые символы.'
            )
        return cocktail_name_translit

    def clean_cocktail_anno(self):
        """
        Проверка описания коктейля на русском языке
        """
        cocktail_anno = self.cleaned_data['cocktail_anno']
        if PATTERNS[RUS_ALL].match(cocktail_anno):
            raise forms.ValidationError(
                'В описании коктейля недопустимые символы.'
            )
        return cocktail_anno

    def clean_cocktail_making_anno(self):
        """
        Проверка описания процесса приготовления на русском языке
        """
        cocktail_making_anno = self.cleaned_data['cocktail_anno']
        if PATTERNS[RUS_ALL].match(cocktail_making_anno):
            raise forms.ValidationError(
                'В описании процесса приготовления коктейля недопустимые символы.'
            )
        return cocktail_making_anno

    def clean(self):
        """
        Общая валидация полей ввода ингредиентов коктейля.
        """
        required = [0, 1]
        cleaned_data = super().clean()
        for i in range(INGREDIENTS_LIMIT):
            ingredient_input = cleaned_data.get(f'ingredient_input_{i}')
            if PATTERNS[RUS].match(ingredient_input):
                self.add_error(
                    f'ingredient_input_{i}',
                    f'В ингредиенте {i} коктейля недопустимые символы.'
                )
            ingredient_value = cleaned_data.get(f'ingredient_value_{i}')
            if ingredient_value and int(ingredient_value) != ingredient_value:
                self.add_error(
                    f'ingredient_value_{i}',
                    f'В количестве ингредиента {i} коктейля недопустимые символы.'
                )
            if i in required and not ingredient_input:
                self.add_error(
                    f'ingredient_input_{i}',
                    f'В коктейле должно быть хотя бы два ингредиента. Отсутствует {i + 1}-й.'
                )
            if ingredient_input and not ingredient_value:
                self.add_error(
                    f'ingredient_value_{i}',
                    f'Не указано количество ингредиента {i + 1}.'
                )
        return self.cleaned_data


class SearchForm(forms.Form):
    """
    Форма поиска на сайте
    """
    q = forms.CharField(
        max_length=128,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Поиск рецепта',
                'class': 'search__box',
            },
        )
    )
