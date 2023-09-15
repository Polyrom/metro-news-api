from typing_extensions import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from api.db_adapter import DBAdapter
from settings import get_settings, ProjectSettings

app = FastAPI()


@app.get('/metro/news')
def get_news(settings: Annotated[ProjectSettings, Depends(get_settings)],
             day: int = 1):
    db_adapter = DBAdapter(settings)
    news = db_adapter.get_news_for_days(day)
    response = [news_item.model_dump() for news_item in news]
    return JSONResponse(content=response)
