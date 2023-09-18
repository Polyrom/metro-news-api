import asyncio
from datetime import datetime
from typing import Generator

import aiohttp
import bs4
from bs4 import BeautifulSoup
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy import exc

from db import db_models


METRO_NEWS_URL = 'http://mosday.ru/news/tags.php?metro'
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
}


class MetroNewsParser:
    """
    Manages mosday metro news parsing
    """
    def __init__(self, db: Session):
        self.db = db
        self.task_active = True

    @staticmethod
    async def _make_request(url) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                logger.debug(f'Requesting {url}')
                response = await resp.text()
                return response

    async def parse_news(self) -> list[dict[str, str]]:
        """
        Parses mosday metro news page
        :return: mapped news items
        """
        news_page_text = await self._make_request(METRO_NEWS_URL)
        html = BeautifulSoup(news_page_text, 'html.parser')
        news_items = self._extract_news_from_page(html)
        mapped_news = [news_item for news_item in self._map_news(news_items)]
        return mapped_news

    @staticmethod
    def _extract_news_from_page(html: BeautifulSoup) -> bs4.ResultSet:
        """
        Extracts the table containing news from the news page
        """
        news_table = html.find(
            "table",
            {'style': 'font-family:Arial;font-size:15px'}
        )
        return news_table.find_all('tr')

    @staticmethod
    def _map_news(news_items: bs4.ResultSet) -> Generator[dict[str, str], None, None]:
        """
        Generator to map news items and specify headline, image URL and publish date
        """
        for news_item in news_items:
            img = news_item.find('img', src=True)
            news_items_properties = news_item.find_all('b')
            try:
                date, headline = news_items_properties
            except ValueError:
                date, _, headline = news_items_properties
            news_item_payload = {
                'headline': headline.text,
                'date_published': datetime.strptime(date.text, '%d.%m.%Y'),
                'image_url': img.get('src') if img else None
            }
            yield news_item_payload

    def _persist_news_to_db(self, news: list[dict[str, str]]) -> None:
        """
        Writes news to database
        :param news: news items
        """
        news_saved = 0
        for news_item in news:
            db_news = db_models.NewsItem(**news_item)
            try:
                self.db.add(db_news)
                self.db.commit()
                news_saved += 1
            except exc.IntegrityError:
                self.db.rollback()
                continue
        logger.debug(f'{news_saved} news items saved to DB')

    async def start_periodic_parsing(self) -> None:
        """
        Parses and writes metro news from mosday to DB every 10 mins
        """
        while self.task_active:
            news = await self.parse_news()
            self._persist_news_to_db(news)
            await asyncio.sleep(30)

    def stop_periodic_parsing(self) -> None:
        self.task_active = False
