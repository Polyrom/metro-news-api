import pytest

from api.db_adapter import DBAdapter


@pytest.fixture(autouse=True)
def fake_api_db_adapter_get_news_for_days(mocker):
    mock_get_news_for_days = mocker.patch.object(
        DBAdapter,
        'get_news_for_days',
        return_value=(('1', 'News item', '12.09.2023', 'https://img.url'),)
    )
    yield mock_get_news_for_days
