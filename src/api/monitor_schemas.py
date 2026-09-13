from pydantic import BaseModel, Field
import datetime

class MonitorAddSchema(BaseModel):
    user_id: int

    name: str = Field(max_length=50)
    url: str

class MonitorSchema(BaseModel):
    id: int
    name: str = Field(max_length=50)
    url: str
    created_at: datetime.datetime
    user_id: int

class MonitorChangeSchema(BaseModel):
    id: int
    name: str = Field(max_length=50)
    url: str

