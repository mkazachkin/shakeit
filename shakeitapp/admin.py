from django.contrib import admin

from shakeitapp.models import DCocktailGroups, DIngredientsGroups, DUnits, TCocktail, TIngredients, \
    TCocktailIngredients, LLikes, LViews, TGenIngredientsImages


@admin.action(description='Одобрить изображения')
def approve_images(modeladmin, request, queryset):
    queryset.update(gi_status=TGenIngredientsImages.ImageStatus.APPROVED)


@admin.action(description='Отклонить изображения')
def disapprove_images(modeladmin, request, queryset):
    queryset.update(gi_status=TGenIngredientsImages.ImageStatus.DISAPPROVED)


@admin.register(DCocktailGroups)
class DCocktailGroupsAdmin(admin.ModelAdmin):
    list_display = (
        'dcg_name',
        'dcg_url',
        'dcg_order',
    )
    ordering = (
        'dcg_order',
    )


@admin.register(DIngredientsGroups)
class DIngredientsGroupsAdmin(admin.ModelAdmin):
    list_display = (
        'di_name',
        'di_url',
        'di_order',
    )
    ordering = (
        'di_order',
    )


@admin.register(DUnits)
class DUnitsAdmin(admin.ModelAdmin):
    list_display = (
        'du_anno'
    ),
    ordering = (
        'du_anno',
    )


@admin.register(TCocktail)
class TCocktailAdmin(admin.ModelAdmin):
    list_display = (
        'cocktail_name',
        'cocktail_group',
        'cocktail_author',
    )
    ordering = (
        'cocktail_name',
    )
    list_filter = (
        'cocktail_group',
    )
    search_fields = (
        'cocktail_anno',
        'cocktail_making',
    )
    search_help_text = 'Поиск по полям описания и процесса приготовления'


@admin.register(TIngredients)
class TIngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient_name',
        'ingredient_group',
    )
    ordering = (
        'ingredient_name',
    )
    list_filter = (
        'ingredient_group',
    )
    search_fields = (
        'ingredient_name',
    )
    search_help_text = 'Поиск по названию'


@admin.register(TCocktailIngredients)
class TCocktailIngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'ci_cocktail',
        'ci_ingredient',
        'ci_quantity',
        'ci_unit',
    )
    ordering = (
        'ci_cocktail',
    )
    search_fields = (
        'ci_cocktail__cocktail_name',
        'ci_ingredient__ingredient_name',
    )
    search_help_text = 'Поиск по названию коктейля или ингредиента'


@admin.register(LLikes)
class LLikesAdmin(admin.ModelAdmin):
    list_display = (
        'll_user',
        'll_cocktail',
        'll_is_like',
    )
    search_fields = (
        'll_user__username',
        'll_cocktail__cocktail_name',
    )
    search_help_text = 'Поиск по названию коктейля или имени пользователя'


@admin.register(LViews)
class LViewsAdmin(admin.ModelAdmin):
    list_display = (
        'lv_date',
        'lv_cocktail',
        'lv_quantity',
    )
    list_filter = (
        'lv_date',
    )
    ordering = (
        '-lv_date',
    )
    search_fields = (
        'lv_cocktail__cocktail_name',
    )
    search_help_text = 'Поиск по названию коктейля'


@admin.register(TGenIngredientsImages)
class TGenIngredientsImagesAdmin(admin.ModelAdmin):
    list_display = (
        'gi_ingredient',
        'gi_status',
        'gi_date_add',
    )
    list_filter = (
        'gi_status',
        'gi_date_add',
    )
    ordering = (
        '-gi_date_add',
    )
    search_fields = (
        'gi_ingredient__ingredient_name',
    )
    search_help_text = 'Поиск по ингредиенту'
    actions = (
        approve_images,
        disapprove_images,
    )
