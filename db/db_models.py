from sqlalchemy import Column, Integer, String, DATE, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class NewsItem(Base):
    __tablename__ = 'metro_news'

    id = Column(Integer, primary_key=True, index=True)
    headline = Column(String)
    image_url = Column(String)
    date_published = Column(DATE)

    __table_args__ = (
        UniqueConstraint('headline'),
    )
