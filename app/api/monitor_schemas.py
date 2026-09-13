from pydantic import BaseModel, Field
import datetime

class MonitorAddSchema(BaseModel):
    user_id: int

    name: str = Field(max_length=50)
    url: str

class MonitorSchema(MonitorAddSchema):
    id: int

    created_at: datetime.datetime

class MonitorChangeSchema(BaseModel):
    id: int
    name: str = Field(max_length=50)
    url: str

