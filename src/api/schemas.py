from pydantic import BaseModel, Field, AnyHttpUrl
from src.database.models import dns_or_https
import datetime

class MonitorAddSchema(BaseModel):
    type_of_request: dns_or_https
    name: str = Field(max_length=50)
    url: AnyHttpUrl
    interval_minutes: int = Field(ge=3)

class MonitorSchema(BaseModel):
    id: int
    type_of_request: dns_or_https
    name: str = Field(max_length=50)
    url: AnyHttpUrl
    interval_min: int = Field(ge=3)
    next_check_at: datetime.datetime
    user_id: int

class MonitorChangeSchema(BaseModel):
    id: int
    name: str = Field(max_length=50)
    url: AnyHttpUrl
    interval_minutes: int = Field(ge=3)

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

class UserUpdateSchema(BaseModel):
    new_username: str = Field(max_length=50)
    new_password: str
