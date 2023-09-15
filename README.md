![flake8](https://github.com/Polyrom/metro-news-api/actions/workflows/linter.yml/badge.svg) ![tests](https://github.com/Polyrom/metro-news-api/actions/workflows/tests.yml/badge.svg)

### Описание
Сервис парсит новости со страницы `http://mosday.ru/news/tags.php?metro` 
и предоставляет базовый REST API для получения этих новостей за период времени.

### Стек
+ Python 3.11
+ FastAPI
+ SQLite

### Запуск
**_Docker_**

1. Создайте образ из корневой директории
```bazaar
docker build -t metro_news_api .
```
2. Запустите контейнер
```bazaar
docker run -d -p 8050:8050 metro_news_api
```
3. REST API будет доступно по адресу:
```bazaar
http://127.0.0.1:8000
```
**_Вне контейнера_**
1. Установите следующие переменные окружения (или пропишите их в `.env`):
```bazaar
HOST=localhost
PORT=8050
SQLITE_DB=random.db
```
2. Из корневой директории запустите проект
```bazaar
python ./main.py
```
### Детали
Реализован эндпоинт, который возвращает список новостей за указанное 
количество дней (включительно). При отсутствии query-параметра 
возвращает новости за последние сутки.
```bazaar
GET /metro/news?day=3
```
Интерактивная OpenAPI документация доступна по адресу:
```bazaar
GET /docs
```