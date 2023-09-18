![flake8](https://github.com/Polyrom/metro-news-api/actions/workflows/linter.yml/badge.svg) ![tests](https://github.com/Polyrom/metro-news-api/actions/workflows/tests.yml/badge.svg)

### Описание
Сервис парсит новости со страницы `http://mosday.ru/news/tags.php?metro` 
и предоставляет базовый REST API для получения этих новостей за период времени.

### Стек
+ Python 3.11
+ FastAPI
+ Postgres

### Запуск
**_Docker_**

1. Создайте образы из корневой директории
```bazaar
docker-compose build
```
2. Запустите контейнеры
```bazaar
docker-compose up -d
```
3. REST API будет доступно по адресу:
```bazaar
http://127.0.0.1:8000
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