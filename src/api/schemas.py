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

class CheckSchema(BaseModel):
    id: int
    monitor_id: int
    status_code: int
    response_time_ms: str
    success: bool
    reason: str
    created_at: datetime.datetime

class LogsInPeriodSchema(BaseModel):
    monitor_id: int
    period_start: datetime.datetime
    period_end: datetime.datetime

class UserLoginSchema(BaseModel):
    username: str = Field(max_length=50)
    password: str
    