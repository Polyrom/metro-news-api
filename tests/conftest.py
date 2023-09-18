import datetime

import pytest

from api.db_adapter import DBAdapter
from db.db_models import NewsItem


@pytest.fixture(autouse=True)
def fake_api_db_adapter_get_news_since_date(mocker):
    mock_get_news_since_date = mocker.patch.object(
        DBAdapter,
        'get_news_since_date',
        return_value=[
            NewsItem(
                headline='News item',
                date_published=datetime.datetime(2023, 9, 12),
                image_url='https://img.url'
            )
        ]
    )
    yield mock_get_news_since_date
