from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from api import utils, schemas
from api.db_adapter import DBAdapter
from db.database import get_db

app = FastAPI()


@app.get('/metro/news', response_model=list[schemas.NewsItemBase])
def get_news_new(db: Session = Depends(get_db),
                 day: int = 1):
    date_from = utils.calculate_date_since(day)
    response = DBAdapter(db).get_news_since_date(date_from)
    return response
