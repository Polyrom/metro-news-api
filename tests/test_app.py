from fastapi.testclient import TestClient

from api.app import app
from db.database import get_db

client = TestClient(app)


def get_fake_db():
    return None


app.dependency_overrides[get_db] = get_fake_db


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
