# Проект &laquo;Сайт рецептов&raquo; на Django
Проект выполнен в качестве задания на итоговой аттестации по программе &laquo;Веб-разработка на Python&raquo; студентом GeekBrains Казачкиным М. Ю.

## Краткое описание проекта
Проект написан на Python 3 (тестировалось на 3.9.18) с использованием фреймворка Django и дополнительных библиотек Python.

Основное приложение (shakeitapp) предполагает следующую функциональность:
* На главной странице демонстрируются 5 самых просматриваемых рецептов в неделю, месяц, год
* Пользователи могут просматривать рецепты коктейлей
* Пользователи могут искать рецепты коктейлей
    * Поисковая строка находится в верхней части каждой страницы
    * Пользователь может воспользоваться каталогом вида коктейля
    * Пользователь может воспользоваться каталогом ингредиентов
* Пользователи могут регистрироваться на сайте
* Зарегистрированные пользователи могут добавлять рецепты на сайт
* Зарегистрированные пользователи могут добавлять рецепты в закладки, доступные для просмотра в личном кабинете
* Администратор сайта может редактировать каталоги и таблицы в панели администратора
* Администратор сайта может запустить генерацию изображений ингредиентов нейросетью Kandinsky, при наличии доступа к API нейросети (требуется регистрация)

API реализовано с помощью фреймворка REST и предполагает следующую функциональность
* Информация о лайках (закладках) предоставляется через REST API (приложение shakeitapi) для авторизованных пользователей
* Информацию о видах ингредиентов из каталога
* Информацию о видах коктейлей из каталога
* Информацию об используемых единицах измерения в рецептах

## Требования к системе пользователя
Для нормального использования сайта на стороне пользователя должны быть выполнены следующие условия:
* В браузере должно быть разрешено сохранение cookie (для сохранения сессии пользователя на сайте)
* В браузере должна быть включена поддержка JavaScript (для работы формы добавления рецепта и демонстрации 5 самых просматриваемых рецептов)

## Установка проекта
Процесс установки описан для систем с ОС Linux и тестировался на Альт Рабочая станция 10. В другом окружении процесс установки не должен отличаться, но некоторые команды будут выполняться иначе. Так, в Windows, вместо команды `python3` вводится команда `python`, а для разделения каталогов при написании путей используется символ обратного деления `\` вместо `/`. Для установки проекта на сайт необходимо выполнить следующие действия:
1. Скачать последнюю версию проекта с GitHub
`git clone https://github.com/mkazachkin/shakeit`
2. При необходимости изменить настройки приложения в файле `settings.py`, расположенном в каталоге приложения `shakeit/shakeit/shakeitapp/`.
3. Создать копию файла `secrets.template.py`, расположенного в каталоге `shakeit/shakeit/shakeitapp/` под именем `secrets.py` в том же каталоге. Для генерации изображения ингредиентов нейросетью Kandinsky получить аутентификационные токены на сайте [Fusion Brain](https://fusionbrain.ai/) и внести их в файл `secrets.py`.
4. Создать виртуальное окружение Python
`python3 -m venv /путь/к/новому/виртуальному/окружению`.
Например, если вы находитесь в каталоге корневом каталоге проекта `shakeit`, достаточно выполнить команду `python3 -m venv ./.venv`.
5. Дальнейшие действия производить с активированным виртуальным окружением. Если вы создали виртуальное окружение в каталоге проекта, то находясь в нем же, виртуальное окружение активируется командой `source ./venv/bin/activate`.
Подробная документация о виртуальном окружении и методах активации в других ОС доступна на [официальном сайте](https://docs.python.org/3/library/venv.html) Python.
6. Дальнейшие действия производить в каталоге `shakeit/shakeit/`
7. Создать каталог для хранения лог файлов командой `md logs` и сам лог-файл командой `touch logs/django.log`. Если логирование не требуется, или есть потребность изменить местоположение лог-файла, необходимо внести соответствующие изменения в глобальные настройки проекта в файле `settings.py` расположенного в каталоге `shakeit/shakeit/shakeit/`.
8. Установить необходимые для работы приложения модули Python
```
pip install -r requirements.txt
```
9. Произвести инициализацию базы данных приложения, выполнив команды в каталоге `shakeit/shakeit/`
```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py initdb
```
10. Если настроен доступ к нейросети Kandinsky, сгенерировать персональные изображения для базовых ингредиентов. Убедится, что доступ по API работает корректно.
```
python3 manage.py bettercallkandinsky
```
11. Запуск приложения.
    a. Запуск приложение в тестовом режиме средствами Django осуществляется командой `python3 manage.py runserver`. Тестовый режим предназначен исключительно для проверки работоспособности приложения. Использование тестового режима для эксплуатации приложения не допускается.
    b. Перед запуском приложения на сервер необходимо внести соотвествующие окружению настройки в файл `settings.py` проекта, обеспечивающие его безопасность.
12. Перейти по адресу на сайте `/admin/` войти под учетной записью `admin` с паролем `admin`. Сменить в панели администратора имя и пароль суперпользователя. Убедится, что таблицы созданы и начальные данные в них присутствуют.
13. Если были сгенерированы персональные изображения ингредиентов, просмотреть таблицу изображений ингредиентов и установить им статус `Одобрено`, чтобы они отображались на сайте. Для повторной генерации изображений в будущем установить статус `Отклонено`. Настроить автоматическое выполнение команды `python3 manage.py bettercallkandinsky` при необходимости.
14. Перейти на главную страницу сайта и убедится, что сайт функционирует нормально.

## История изменений
14.04.2024. Полностью реализован базовый функционал.

## Дорожная карта
Доработки пока не запланированы.

## Информация для связи и авторские права
Все изображения базовой версии сгенерированы с помощью нейросети Kandinsky ([Fusion Brain](https://fusionbrain.ai/)) или созданы автором.

Дизайн, логотип созданы автором.

Исходные коды размещены на сервисе [GitHub](https://github.com/mkazachkin/shakeit).

---

&copy;&nbsp;2024 Михаил Казачкин.
