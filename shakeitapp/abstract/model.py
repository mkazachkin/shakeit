from django.db import models, connection


class ModelWTruncate(models.Model):
    """
    Абстрактный базовый класс модели.
    Добавляет в базовую модель Django метод Truncate для опустошения таблиц,
    а также поле objects, для нормальной поддержки со стороны PyCharm Community Edition
    """
    objects = models.Manager()

    class Meta:
        abstract = True

    @classmethod
    def truncate(cls, sqlite: bool = True):
        """
        Очищает таблицу в БД.
        Аргументы:
            sqlite: bool - индикатор СУБД SQLite. Включен по-умолчанию.
        """
        with connection.cursor() as cursor:
            if sqlite:
                cursor.execute('DELETE FROM {0};'.format(cls._meta.db_table))
            else:
                cursor.execute('TRUNCATE TABLE {0} CASCADE;'.format(cls._meta.db_table))
