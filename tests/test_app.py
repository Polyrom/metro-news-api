from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


def test_read_main():
    response = client.get("/metro/news")
    assert response.status_code == 200
    assert response.json() == [
        {
            'headline': 'News item',
            'date_published': '2023-09-12',
            'image_url': 'https://img.url'
        }
    ]
