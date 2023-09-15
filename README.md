[![linter](https://github.com/Polyrom/metro-news-api/actions/workflows/linter.yml/badge.svg)]

### Описание
Сервис парсит новости со страницы `http://mosday.ru/news/tags.php?metro` 
и предоставляет базовый REST API для получения этих новостей за период времени.

### Стек
+ Python 3.11
+ FastAPI
+ SQLite

### Запуск
1. Популируйте .env файл: укажите хост, порт и название файла SQLite. 
Образец можно найти в файле `.env.example`
2. Создайте образ:
```bazaar
docker build -t metro_news_api .
```
3. Запустите контейнер:
```bazaar
docker run -p 8000:{порт из вашего .env} metro_news_api
```
4. REST API будет доступно по адресу:
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