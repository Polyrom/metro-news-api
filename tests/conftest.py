import pytest

from api.db_adapter import DBAdapter
from api.models import NewsItem


@pytest.fixture(autouse=True)
def fake_api_db_adapter_get_news_for_days(mocker):
    mock_get_news_for_days = mocker.patch.object(
        DBAdapter,
        'get_news_for_days',
        return_value=[
            NewsItem(
                headline='News item',
                date_published='2023-09-12',
                image_url='https://img.url'
            )
        ]
    )
    yield mock_get_news_for_days
