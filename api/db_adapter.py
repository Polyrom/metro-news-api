from api import utils
from db import sql_queries
from db.database import DataBase
from settings import ProjectSettings


class DBAdapter:
    """
    Manages API communication with database
    """

    def __init__(self, settings: ProjectSettings):
        self.settings = settings

    def get_news_for_days(self, days: int) -> tuple[str]:
        """
        Gets rows of news from database for a defined number of days
        :param days: number of days
        :return:
        """
        date_since = utils.calculate_date_since_days(days)
        db = DataBase(self.settings.sqlite_db)
        db.connect()
        news = db.fetch_data(
            query=sql_queries.SELECT_NEWS_SINCE_DATE,
            params=[date_since]
        )
        db.close()
        return news
