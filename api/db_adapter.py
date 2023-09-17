from datetime import date

from sqlalchemy.orm import Session

from db import db_models


class DBAdapter:
    """
    Manages API communication with database
    """

    def __init__(self, db: Session):
        self.db = db

    def get_news_since_date(self, date_from: date) -> list[db_models.NewsItem]:
        """
        Gets news from DB since and including the specified date
        :param date_from: start date
        :return: a list of news items
        """
        return self.db.query(db_models.NewsItem).filter(db_models.NewsItem.date_published >= date_from).all()
