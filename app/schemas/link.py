from pydantic import BaseModel, HttpUrl
from datetime import datetime


class LinkCreate(BaseModel):
    original_url: HttpUrl


class LinkResponse(BaseModel):
    id: int
    original_url: HttpUrl
    short_code: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True
class LinkList(BaseModel):
    id: int
    original_url: HttpUrl
    short_code: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True

class LinkUpdate(BaseModel):
    original_url: HttpUrl
    
class LinkStats(BaseModel):
    total_links: int
    total_clicks: int
    most_clicked_link: str | None