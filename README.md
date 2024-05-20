# QRKot

## О проекте

**QRkot** - это API сервиса по сбору средств для финансирования  Благотворительного фонда поддержки котиков.Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции. 

В сервисе реализована возможность регистрации пользователей, добавления благотворительных проектов и пожертвований, которые распределяются по открытым проектам.

Настроено автоматическое создание первого суперпользователя при запуске проекта.

Добавлена возможность формирования отчёта в гугл-таблице с помощью сервисов Google Cloud Platform:
- Google Sheets API - управление электронными таблицами
- Google Drive API - упрвление файлами на гугл-диске

## Автор проекта:
Валерий Шанкоренко<br/>
Github: [Valera Shankorenko](https://github.com/valerashankorenko)<br/>
Telegram:[@valeron007](https://t.me/valeron007)<br/>
E-mail:valerashankorenko@yandex.by<br/>

## Стек технологий
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://pypi.org/project/alembic/)
- [Pydantic](https://pypi.org/project/pydantic/)
- [Asyncio](https://docs.python.org/3/library/asyncio.html)
- [Google Cloud Platform](https://cloud.google.com/docs)
- [Google Sheets API](https://developers.google.com/sheets/api/guides/concepts?hl=ru)
- [Google Drive API](https://developers.google.com/drive/api/guides/about-sdk?hl=ru)

## Как запустить проект:
1. Клонировать репозиторий и перейти в его директорию в командной строке:
```shell
git clone git@github.com:valerashankorenko/QRkot_spreadsheets.git
```
```shell
cd QRkot_spreadsheets
```
2. Cоздать и активировать виртуальное окружение:
 - для Linux/MacOS
```shell
python3 -m venv venv
source venv/bin/activate
```
- для Windows
```shell
python -m venv venv
source venv/Scripts/activate
```
3. Обновить пакетный менеджер pip
```shell
python3 -m pip install --upgrade pip
```
4. Установить зависимости из файла requirements.txt:
```shell
pip install -r requirements.txt
```
5. Создайте в корневой директории файл .env со следующим наполнением:
```
APP_TITLE=Приложение QRKot.
APP_DESC=Благотворительный фонд для сбора пожертвований.
DATABASE_URL=sqlite+aiosqlite:///./<название базы данных>.db
SECRET=<секретное слово>
FIRST_SUPERUSER_EMAIL=<email суперюзера>
FIRST_SUPERUSER_PASSWORD=<пароль суперюзера>
#Вводим данные сервисного гугл аккаунта
TYPE=service_account
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
UNIVERSE_DOMAIN=
EMAIL=email гугл аккаунта
```
6. Автоматическое создание файла миграции для базы данных SQLite:
```shell
alembic revision --autogenerate -m "Название миграции" 
```
7. Применение всех неприменённых миграций:
```shell
alembic upgrade head
```
8. Запуск проекта:
```shell
uvicorn app.main:app --reload
```
Проект будет запущен и доступен по следующим адресам:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs - автоматически сгенерированная документация Swagger
- http://127.0.0.1:8000/redoc - автоматически сгенерированная документация ReDoc
- http://127.0.0.1:8000/google - отчет в гугл-таблице

После запуска доступны следующие эндпоинты:
- Регистрация и аутентификация:
    - **/auth/register** - регистрация пользователя
    - **/auth/jwt/login** - аутентификация пользователя (получение jwt-токена)
    - **/auth/jwt/logout** - выход (сброс jwt-токена)
- Пользователи:
    - **/users/me** - получение и изменение данных аутентифицированного пользователя
    - **/users/{id}** - получение и изменение данных пользователя по id
- Благотворительные проекты:
    - **/charity_project/** - получение списка проектов и создание нового
    - **/charity_project/{project_id}** - изменение и удаление существующего проекта
- Пожертвования:
    - **/donation/** - получение списка всех пожертвований и создание пожертвования
    - **/donation/my** - получение списка всех пожертвований аутентифицированного пользователя
- GoogleAPI:
    - **/google/** - создание отчёта в гугл-таблице
