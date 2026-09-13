from pydantic import BaseModel, Field
import datetime

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

