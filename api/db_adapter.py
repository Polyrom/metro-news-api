from typing import Generator

from api import utils
from api.models import NewsItem
from db import sql_queries
from db.database import DataBase
from settings import ProjectSettings


class DBAdapter:
    """
    Manages API communication with database
    """

    def __init__(self, settings: ProjectSettings):
        self.settings = settings

    def _fetch_news_from_db_since_date(self, date_from: str) -> tuple[str]:
        """
        Gets rows of news since and including the date
        :param date_from: date from which news should be extracted
        :return: rows of news
        """
        db = DataBase(self.settings.sqlite_db)
        db.connect()
        news = db.fetch_data(
            query=sql_queries.SELECT_NEWS_SINCE_DATE,
            params=[date_from]
        )
        db.close()
        return news

    def get_news_for_days(self, days: int) -> list[NewsItem]:
        """
        Gets news from DB for the number of days
        :param days: number of days
        :return: news_item
        """
        date_from = utils.calculate_date_since_days(days)
        news_rows = self._fetch_news_from_db_since_date(date_from)
        news_for_days = []
        for row in news_rows:
            news_item = NewsItem(
                headline=row[1],
                date_published=utils.normalize_date_for_response(row[2]),
                image_url=row[3]
            )
            news_for_days.append(news_item)
        return news_for_days

