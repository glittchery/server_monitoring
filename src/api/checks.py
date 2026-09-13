from src.services.check_service import CheckService
from fastapi import APIRouter, Depends
from typing import Annotated
from src.api.schemas import CheckSchema, LogsInPeriodSchema

checks_router = APIRouter(
    prefix="/checks",
    tags=["Checks API"]
)

@checks_router.post("")
async def perform_check(monitor_id: int):
    await CheckService.perform_check(monitor_id)
    return {"success": True}

@checks_router.get("")
async def get_logs(data: Annotated[LogsInPeriodSchema, Depends()]) -> list[Annotated[CheckSchema, Depends()]]:
    result = await CheckService.get_logs(data.monitor_id, data.period_start, data.period_end)
    return result

@checks_router.delete("")
async def delete_logs(data: Annotated[LogsInPeriodSchema, Depends()]):
    await CheckService.delete_logs(data.monitor_id, data.period_start, data.period_end)
    return {"success": True}


