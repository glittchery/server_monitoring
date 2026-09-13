from pydantic import BaseModel, Field
from src.database.models import dns_or_https
import datetime

class MonitorAddSchema(BaseModel):
    user_id: int

    type_of_request: dns_or_https
    name: str = Field(max_length=50)
    url: str

class MonitorSchema(BaseModel):
    id: int
    user_id: int
    type_of_request: dns_or_https
    name: str = Field(max_length=50)
    url: str
    created_at: datetime.datetime

class MonitorChangeSchema(BaseModel):
    id: int
    name: str = Field(max_length=50)
    url: str

