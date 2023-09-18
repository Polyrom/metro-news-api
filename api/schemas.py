from pydantic import BaseModel, NaiveDatetime, ConfigDict, field_serializer

from api.utils import convert_date_to_ymd


class NewsItemBase(BaseModel):
    headline: str
    image_url: str | None
    date_published: NaiveDatetime

    @field_serializer('date_published')
    def serialize_date_published(self, dt: NaiveDatetime, _info):
        return convert_date_to_ymd(dt)

    model_config = ConfigDict(from_attributes=True)
