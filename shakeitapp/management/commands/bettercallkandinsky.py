import logging
import time
import json
import base64
from typing import Optional

import requests
from django.core.files.base import ContentFile
from django.core.management import BaseCommand
from django.utils import timezone

from shakeitapp.models import TIngredients, TGenIngredientsImages
from shakeitapp.settings import KANDINSKY_GENERATE_URL, KANDINSKY_CHECK_URL, \
    KANDINSKY_HEADERS, KANDINSKY_MODEL_URL, KANDINSKY_IMAGE_WIDTH, KANDINSKY_IMAGE_HEIGHT, KANDINSKY_IMAGE_NUM, \
    KANDINSKY_WAITING_TIME, KANDINSKY_GET_ATTEMPTS

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Обращается по API к нейросети Kandinsky и генерирует изображения ингредиентов
    для определенных категорий
    """
    help = 'Получает сгенерированные изображения ингредиентов от нейросети Сбера.'
    images_width = KANDINSKY_IMAGE_WIDTH
    images_height = KANDINSKY_IMAGE_HEIGHT
    images_num = KANDINSKY_IMAGE_NUM
    model_url = KANDINSKY_MODEL_URL
    model_id = None
    gen_url = KANDINSKY_GENERATE_URL
    gen_headers = KANDINSKY_HEADERS
    gen_check_url = KANDINSKY_CHECK_URL
    gen_check_delay = KANDINSKY_WAITING_TIME
    gen_attempts = KANDINSKY_GET_ATTEMPTS

    def handle(self, *args, **options):
        self.get_model()
        ingredients = TIngredients.objects.all()
        for ingredient in ingredients:
            image_for_generating = TGenIngredientsImages.objects \
                .filter(gi_ingredient=ingredient) \
                .exclude(gi_status=TGenIngredientsImages.ImageStatus.DISAPPROVED)
            if not image_for_generating:
                image_for_generating = TGenIngredientsImages(
                    gi_ingredient=ingredient,
                    gi_date_add=timezone.now(),
                )
                image_for_generating.save()
        generating_list = TGenIngredientsImages.objects \
            .filter(gi_status=TGenIngredientsImages.ImageStatus.INITIATED)
        logger.info(f'Список объектов генерации обновлен.')
        if not generating_list:
            logger.info('Генерировать нечего. Выхожу.')
        for newbie_image in generating_list:
            ingredient = TIngredients.objects \
                .filter(id=newbie_image.gi_ingredient_id) \
                .first()
            # Возможно, имеет смысл поэкспериментировать с запросом к нейросети
            prompt = f'{ingredient.ingredient_name} на столе в шикарном ресторане'
            job_uuid = self.send_image_prompt(prompt)
            response = None
            if job_uuid:
                response = self.get_image(job_uuid)
            if not response:
                logger.warning(f'Не удалось получить ответ на запрос генерации {ingredient.ingredient_name}.')
                pass
            elif response['status'] == 'DONE':
                for i in range(self.images_num):
                    try:
                        image_data = response['images'][i]
                    except IndexError:
                        logger.warning(f'Изображение {i} не найдено в ответе на запрос.\n')
                        break
                    image_ext = 'jpg'
                    file_name = f'{ingredient.ingredient_url}_{i}.{image_ext}'
                    image_data = ContentFile(base64.b64decode(image_data), name=file_name)
                    image_record = newbie_image
                    if i > 1:
                        image_record.pk = None
                    image_record.gi_image = image_data
                    image_record.gi_date_done = timezone.now()
                    image_record.gi_status = TGenIngredientsImages.ImageStatus.GENERATED
                    if response['censored']:
                        logger.warning(f'Запрос не прошел цензуру.\n')
                        image_record.gi_censored = True
                        image_record.gi_status = TGenIngredientsImages.ImageStatus.CENSORED
                    image_record.save()
                    logger.info(f'Изображение {i} для {ingredient.ingredient_name} сгенерировано.\n')
            else:
                status = response['status']
                error = response['errorDescription']
                logger.error(f'Ошибка генерации изображения {ingredient.ingredient_name}: '
                             f'{error}. Статус: {status}\n')

    def send_image_prompt(self, prompt: str) -> Optional[str]:
        """
        Отправляет запрос на генерацию изображения в API
        Аргументы:
            prompt: str - текстовый запрос на генерацию
        Возвращает:
            str - текстовое представление идентификатора процесса UUID
        """
        params = {
            'type': 'GENERATE',
            'numImages': self.images_num,
            'width': self.images_width,
            'height': self.images_height,
            'generateParams': {
                'query': f'{prompt}',
            },
        }

        data = {
            'model_id': (None, self.model_id),
            'params': (None, json.dumps(params), 'application/json'),
        }
        response = requests.post(self.gen_url, headers=self.gen_headers, files=data)
        data = response.json()
        try:
            return data['uuid']
        except KeyError:
            logger.error(f"Ошибка отправления запроса на генерацию. "
                         f"Статус: {data['status']}\n")
            return None

    def get_image(self, request_id: str):
        """
        Получает изображение от нейросети по API в виде JSON
        и возвращает его, если все прошло успешноЮ или None,
        если что-то пошло не так.
        Аргументы:
            request_id: str - текстовое представление UUID запроса не генерацию
        Возвращает:
            json - ответ API нейросети
        """
        attempts = self.gen_attempts
        while attempts > 0:
            logger.info(f'Пытаюсь получить изображение. Осталось попыток {attempts}.\n')
            time.sleep(self.gen_check_delay)
            response = requests.get(f'{self.gen_check_url}{request_id}', headers=KANDINSKY_HEADERS)
            data = response.json()
            if data['status'] == 'DONE' or data['status'] == 'FAIL':
                logger.info(f'Получен ответ на запрос генерации изображения.\n')
                return data
            attempts -= 1
        return None

    def get_model(self):
        """
        Возвращает идентификатор доступной модели
        """
        response = requests.get(self.model_url, headers=self.gen_headers)
        data = response.json()
        try:
            self.model_id = data[0]['id']
            logger.info(f'Получен идентификатор модели.')
        except KeyError:
            logger.critical(f'Не могу получить идентификатор модели. Ответ API: {data}')
            exit()
