from sqlalchemy import Column, Integer, String, DATE, UniqueConstraint

from db.database import Base


class NewsItem(Base):
    __tablename__ = 'metro_news_new'

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String)
    image_url = Column(String)
    date_published = Column(DATE)

    __table_args__ = (
        UniqueConstraint('headline'),
    )
