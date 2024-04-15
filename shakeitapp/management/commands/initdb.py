import logging
import os

from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'sql')

SQL_SCRIPT = [
    'django.user.sql',
    'shakeitapp.dcocktailgroups.sql',
    'shakeitapp.dingredientsgroups.sql',
    'shakeitapp.dunits.sql',
    'shakeitapp.tcocktail.sql',
    'shakeitapp.tingredients.sql',
    'shakeitapp.tcocktailingredients.sql',
    'shakeitapp.lviews.sql',
    'shakeitapp.llikes.sql',
]

SCRIPT_VARIABLES = {
    'now': timezone.now().strftime('%Y-%m-%dT%H:%M:%S'),
    'date': timezone.now().strftime('%Y-%m-%d'),
}

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Добавляет начальные записи в базу данных и суперпользователя
    admin с паролем admin.
    NOTA BENE! При развертывании проекта необходимо сменить имя
    пользователя и пароль через панель администратора.
    """
    help = 'Добавляет в базу данных начальные значения.'

    def handle(self, *args, **options):
        sql_statement = ''
        success = True
        logger.info('Начинаю процесс инициализации базы данных.')
        for script in SQL_SCRIPT:
            logger.info(f'Готовлю данные из {script}')
            script_path = os.path.join(SCRIPT_PATH, script)
            try:
                data = open(script_path).read()
                sql_statement += f'{data}\n'
            except IOError as err:
                logger.critical(f'Ошибка чтения файла. Работа остановлена.\n{err}')
                success = False
                break
        for variable, value in SCRIPT_VARIABLES.items():
            sql_statement = sql_statement.replace('{{ ' + variable + ' }}', value)
        if success:
            logger.info(f'Данные подготовлены.')
            try:
                with connection.cursor() as cursor:
                    cursor.executescript(sql_statement)
            except Exception as err:
                logger.critical(f'Ошибка при добавлении в БД. Работа остановлена.\n{err}')
                success = False
        if success:
            logger.info('Данные инициализированы.')
