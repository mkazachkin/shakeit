import re

from shakeitapp.secrets import KANDINSKY_API_TOKEN, KANDINSKY_SECRET_TOKEN

# Максимальное количество ингредиентов в коктейле на рецепт.
INGREDIENTS_LIMIT = 10

# Коды полей ввода данных в форме.
# Значение кодов не должно находится в диапазоне от 0 до INGREDIENTS_LIMIT.
COCKTAIL_RU_INPUT, COCKTAIL_EN_INPUT = 1001, 1002
COCKTAIL_ANNO, COCKTAIL_MAKING = 1003, 1004

# Коды языков проверки для паттернов проверки
RUS, RUS_ALL, ENG, ENG_ALL, RUSENG_ALL = 0, 1, 2, 3, 4

# Паттерны проверки
PATTERNS = {
    RUS: re.compile(r"[^0-9А-ЯЁа-яё\- ]"),
    RUS_ALL: re.compile(r"[^?!,.:;—–0-9А-ЯЁа-яё\-%\s\n]"),
    ENG: re.compile(r"[^0-9A-Za-z\- ]"),
    ENG_ALL: re.compile(r"[^?!,.:;—–0-9A-Za-z\-%\s\n]"),
    RUSENG_ALL: re.compile(r"[^?!,.:;—–0-9А-ЯЁа-яёA-Za-z\-%\s\n]"),
}

# Количество коктейлей на страницу поиска
PAGE_LIMIT = 10

# Типовое изображение ингредиента
GENERIC_INGREDIENT_IMAGE = 'images/generic_ingredient_img.jpg'

# Настройки API нейросети Kandinsky. Данные для аутентификации настраиваются в файле secrets.py
KANDINSKY_GENERATE_URL = 'https://api-key.fusionbrain.ai/key/api/v1/text2image/run'
KANDINSKY_CHECK_URL = 'https://api-key.fusionbrain.ai/key/api/v1/text2image/status/'
KANDINSKY_MODEL_URL = 'https://api-key.fusionbrain.ai/key/api/v1/models'
KANDINSKY_HEADERS = {
    'X-Key': f'Key {KANDINSKY_API_TOKEN}',
    'X-Secret': f'Secret {KANDINSKY_SECRET_TOKEN}',
}
KANDINSKY_IMAGE_WIDTH = 512
KANDINSKY_IMAGE_HEIGHT = 512
KANDINSKY_IMAGE_NUM = 1
KANDINSKY_WAITING_TIME = 11
KANDINSKY_GET_ATTEMPTS = 10
KANDINSKY_STYLE = 'UHD'
