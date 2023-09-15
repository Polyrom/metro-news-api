from pydantic import BaseModel


class NewsItem(BaseModel):
    headline: str
    image_url: str | None
    date_published: str
