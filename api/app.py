from typing_extensions import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from api import utils
from api.db_adapter import DBAdapter
from api.models import NewsItem
from settings import get_settings, ProjectSettings

app = FastAPI()


@app.get('/metro/news')
def get_news(settings: Annotated[ProjectSettings, Depends(get_settings)],
             day: int = 1):
    db_adapter = DBAdapter(settings)
    news = db_adapter.get_news_for_days(day)
    response = []
    for row in news:
        news_item = NewsItem(
            headline=row[1],
            date_published=utils.normalize_date_for_response(row[2]),
            image_url=row[3]
        )
        response.append(news_item.model_dump())
    return JSONResponse(content=response)
