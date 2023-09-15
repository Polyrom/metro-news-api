from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings

from api.app import app
from settings import ProjectSettings


client = TestClient(app)


class FakeProjectSettings(BaseSettings):
    host: str
    port: int
    sqlite_db: str


def get_fake_settings():
    return FakeProjectSettings(
        host='fake_host',
        port=9999,
        sqlite_db='fake.db'
    )


app.dependency_overrides[ProjectSettings] = get_fake_settings


def test_get_news():
    response = client.get("/metro/news")
    assert response.status_code == 200
    assert response.json() == [
        {
            'headline': 'News item',
            'date_published': '2023-09-12',
            'image_url': 'https://img.url'
        }
    ]
