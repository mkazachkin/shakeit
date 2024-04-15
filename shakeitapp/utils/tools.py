from uuid import NAMESPACE_OID, uuid5, UUID
from datetime import datetime, timezone, timedelta


CURRENT_TIMEZONE = 'MSK'
TIMEZONES = {
    'EET': 2,   # MSK-1. Калининград, Eastern European Time
    'MSK': 3,   # MSK+0. Московское время, Moscow Standard Time
    'SAMT': 4,  # MSK+1. Самарское время, Samara Time
    'YEKT': 5,  # MSK+2. Екатеринбургское время, Yekaterinburg Time
    'OMST': 6,  # MSK+3. Омское время, Omsk Standard Time
    'KRAT': 7,  # MSK+4. Красноярское время, Krasnoyarsk Time
    'NOVT': 7,  # MSK+4. Новосибирское время, Novosibirsk Time
    'IRKT': 8,  # MSK+5. Иркутское время, Irkutsk Time
    'YAKT': 9,  # MSK+6. Якутское время, Yakutsk Time
    'VLAT': 10,  # MSK+7. Владивостокское время, Yakutsk Time
    'MAGT': 11,  # MSK+8. Магаданское время, Magadan Time
    'SAKT': 11,  # MSK+8. Сахалинское время, Sakhalin Time
    'SRET': 11,  # MSK+8. Среднеколымское время, Srednekolymsk Time
    'ANAT': 12,  # MSK+9. Анадырское время, Anadyr Time
    'PETT': 12,  # MSK+9. Камчатское время, Kamchatka Time
}


def string_to_uuid(usr_string: str, lower_case: bool = True, no_spaces: bool = True) -> UUID:
    """
    Генерирует уникальный идентификатор для строки формата uuid5 с использованием ISO OID.
    Одинаковые строки будут иметь одинаковый UUID.
    Аргументы:
        usr_string: str - строка
        lower_case: bool - преобразовывать строку в нижний регистр
        no_spaces: bool - убирать из строки пробелы
    Возвращает:
        string_to_uuid: UUID - сгенерированный UUID
    """
    result_string: str = usr_string
    if lower_case:
        result_string = result_string.lower()
    if no_spaces:
        result_string = result_string.replace(' ', '')
    return uuid5(NAMESPACE_OID, result_string)


def ru_string_translit(ru_str: str) -> str:
    """
    Транслитерирует строку на русском языке по ГОСТ 7.79-2000 системе Б
    Аргументы:
        ru_str: str - строка на русском языке
    Возвращает:
        ru_string_translit: str - транслитерированная строка
    """
    result = ru_str
    translit_dict = {
        'ЦИ': 'CI',
        'Ци': 'Ci',
        'ци': 'ci',
        'цИ': 'cI',
        'ЦЕ': 'CE',
        'Це': 'Ce',
        'це': 'ce',
        'цЕ': 'cE',
        'ЦЁ': 'CYo',
        'Цё': 'Cyo',
        'цё': 'cyo',
        'цЁ': 'cYo',
        'ЦЫ': 'CY`',
        'Цы': 'Cy`',
        'цы': 'cy`',
        'цЫ': 'cY`',
        'ЦЙ': 'CJ`',
        'Цй': 'Cj`',
        'цй': 'cj`',
        'цЙ': 'cJ`',
        'ЦЭ': 'CE`',
        'Цэ': 'Ce`',
        'цэ': 'ce`',
        'цЭ': 'cE`',
        'ЦЮ': 'CYu',
        'Цю': 'Cyu',
        'цю': 'cyu',
        'цЮ': 'cYu',
        'ЦЯ': 'CYa',
        'Ця': 'Cya',
        'ця': 'cya',
        'цЯ': 'cYa',
        'А': 'A',
        'а': 'a',
        'Б': 'B',
        'б': 'b',
        'В': 'V',
        'в': 'v',
        'Г': 'G',
        'г': 'g',
        'Д': 'D',
        'д': 'd',
        'Е': 'E',
        'е': 'e',
        'Ё': 'Yo',
        'ё': 'yo',
        'Ж': 'Zh',
        'ж': 'zh',
        'З': 'Z',
        'з': 'z',
        'И': 'I',
        'и': 'i',
        'Й': 'J',
        'й': 'j',
        'К': 'K',
        'к': 'k',
        'Л': 'L',
        'л': 'l',
        'М': 'M',
        'м': 'm',
        'Н': 'N',
        'н': 'n',
        'О': 'O',
        'о': 'o',
        'П': 'P',
        'п': 'p',
        'Р': 'R',
        'р': 'r',
        'С': 'S',
        'с': 's',
        'Т': 'T',
        'т': 't',
        'У': 'U',
        'у': 'u',
        'Ф': 'F',
        'ф': 'f',
        'Х': 'X',
        'х': 'x',
        'Ц': 'Cz',
        'ц': 'Cz',
        'Ч': 'Cz',
        'ч': 'cz',
        'Ш': 'Sh',
        'ш': 'sh',
        'Щ': 'Shh',
        'щ': 'shh',
        'Ъ': '``',
        'ъ': '`',
        'Ы': 'Y`',
        'ы': 'y`',
        'Ь': '`',
        'ь': '`',
        'Э': 'E`',
        'э': 'e`',
        'Ю': 'Yu',
        'ю': 'yu',
        'Я': 'Ya',
        'я': 'ya',
    }

    for ru_char, lat_char in translit_dict.items():
        result = result.replace(ru_char, lat_char)

    return result
