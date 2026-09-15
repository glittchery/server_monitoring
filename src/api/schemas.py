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
    name: str | None = Field(default=None, max_length=50)
    url: AnyHttpUrl | None = None
    interval_minutes: int | None = Field(default=None, ge=3)

class CheckSchema(BaseModel):
    id: int
    monitor_id: int
    status_code: int | None
    response_time_ms: str | None
    success: bool
    reason: str
    created_at: datetime.datetime

class LogsInPeriodSchema(BaseModel):
    monitor_id: int
    period_start: datetime.datetime | None = datetime.datetime(2000, 1, 1, 0, 0)
    period_end: datetime.datetime | None = datetime.datetime(2100, 1, 1, 0, 0)

class UserLoginSchema(BaseModel):
    username: str = Field(max_length=50)
    password: str

class UserUpdateSchema(BaseModel):
    new_username: str | None = Field(default=None, max_length=50)
    new_password: str | None = None
