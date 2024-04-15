import logging

from django.contrib.auth.models import User
from rest_framework import serializers
from shakeitapp.models import DUnits, DIngredientsGroups, DCocktailGroups, TCocktail, LLikes


logger = logging.getLogger(__name__)


class UnitsSerializer(serializers.ModelSerializer):
    """
    Преобразует таблицу DUnits в список словарей для последующего преобразования в JSON.
    Описания единиц измерения не включены.
    """
    class Meta:
        model = DUnits
        fields = (
            'id',
            'du_name',
        )


class IngredientsGroupsSerializer(serializers.ModelSerializer):
    """
    Преобразует таблицу DIngredientsGroups в список словарей для последующего преобразования в JSON.
    Описания групп не включены.
    """
    class Meta:
        model = DIngredientsGroups
        fields = (
            'id',
            'di_name',
            'di_name_translit',
            'di_url',
        )


class CocktailGroupsSerializer(serializers.ModelSerializer):
    """
    Преобразует таблицу DCocktailGrups в список словарей для последующего преобразования в JSON.
    Описания групп не включены.
    """
    class Meta:
        model = DCocktailGroups
        fields = (
            'id',
            'dcg_name',
            'dcg_name_translit',
            'dcg_url',
            'dcg_order',
        )


class WriterLikePostSerializer(serializers.Serializer):
    """
    Ставит лайк коктейлю, если его не было, и убирает его, если он был.
    """
    ll_user_id = serializers.HiddenField(default=0)
    ll_cocktail = serializers.PrimaryKeyRelatedField(queryset=TCocktail.objects.all())
    ll_is_like = serializers.BooleanField()

    class Meta:
        model = LLikes

    def update(self, instance, validated_data):
        instance.ll_is_like = validated_data['ll_is_like']
        instance.save()
        return instance

    def create(self, validated_data):
        validated_data['ll_user_id'] = self.context['request'].user.id
        instance = LLikes.objects.filter(
            ll_user_id=validated_data['ll_user_id'],
            ll_cocktail=validated_data['ll_cocktail'],
        ).first()
        if instance:
            return self.update(instance, validated_data)
        return LLikes.objects.create(**validated_data)
