import asyncio
from typing import Generator

import aiohttp
import bs4
from bs4 import BeautifulSoup
from loguru import logger

from db import sql_queries
from db.database import DataBase
from settings import ProjectSettings


class MetroNewsParser:
    """
    Manages mosday metro news parsing
    """
    def __init__(self, settings: ProjectSettings):
        self.settings = settings
        self.metro_news_url = 'http://mosday.ru/news/tags.php?metro'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        }
        self.db = DataBase(self.settings.sqlite_db)
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
        news_page_text = await self._make_request(self.metro_news_url)
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
                'date_published': date.text,
                'image_url': img.get('src') if img else None
            }
            yield news_item_payload

    @staticmethod
    def _prepare_news_for_insert(news: list[dict[str, str]]) -> list[list[str]]:
        """
        Maps news item into a structure that facilitates write to DB
        :param news: mapped list of news items
        :return: list of structures ready for writing to DB
        """
        news_prepared_for_insert = []
        for news_payload in news:
            extracted_news_item = [
                news_payload.get('headline'),
                news_payload.get('date_published'),
                news_payload.get('image_url')
            ]
            news_prepared_for_insert.append(extracted_news_item)
        return news_prepared_for_insert

    def _persist_news_to_db(self, news: list[list[str]]) -> None:
        """
        Writes news items to DB
        """
        self.db.connect()
        try:
            self.db.execute_query("BEGIN TRANSACTION")
            for item in news:
                self.db.execute_query(sql_queries.INSERT_NEWS_ITEM, item)
            self.db.conn.commit()
            logger.debug('News written to DB successfully')
        except Exception as e:
            logger.error(f"Error during news write to DB: {e}")
            self.db.conn.rollback()

    async def start_periodic_parsing(self) -> None:
        """
        Writes metro news from mosday to DB every 10 mins
        :return:
        """
        while self.task_active:
            news = await self.parse_news()
            news_prepared_for_db = self._prepare_news_for_insert(news)
            self._persist_news_to_db(news_prepared_for_db)
            await asyncio.sleep(10 * 60)

    def stop_periodic_parsing(self) -> None:
        self.task_active = False
