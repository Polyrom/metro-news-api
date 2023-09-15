from dataclasses import dataclass
import pytest

from api.db_adapter import DBAdapter


@dataclass
class FakeProjectSettings:
    host: str
    port: int
    sqlite_db: str


@pytest.fixture(autouse=True)
def fake_project_settings(mocker):
    mock_project_settings = mocker.patch(
        'settings.get_settings',
        return_value=FakeProjectSettings(
            host='fake_host',
            port=1111,
            sqlite_db='fake_db.db'
        )
    )
    yield mock_project_settings


@pytest.fixture(autouse=True)
def fake_api_db_adapter_get_news_for_days(mocker):
    mock_get_news_for_days = mocker.patch.object(
        DBAdapter,
        'get_news_for_days',
        return_value=(('1', 'News item', '12.09.2023', 'https://img.url'),)
    )
    yield mock_get_news_for_days
