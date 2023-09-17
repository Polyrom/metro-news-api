from pydantic import BaseModel, NaiveDatetime

from api.utils import convert_date_to_ymd


class NewsItemBase(BaseModel):
    headline: str
    image_url: str | None
    date_published: NaiveDatetime

    class Config:
        from_attributes = True
        json_encoders = {
            NaiveDatetime: convert_date_to_ymd
        }
