from fastapi import APIRouter, Depends
from typing import Annotated

from src.api.monitor_schemas import MonitorAddSchema, MonitorSchema, MonitorChangeSchema
from src.services.monitor_service import MonitorService

monitors_router = APIRouter(
    prefix="/monitors"
)

@monitors_router.post("")
async def add_monitor(monitor: Annotated[MonitorAddSchema, Depends()]):
    await MonitorService.create_monitor(monitor.user_id, monitor.name, monitor.url)
    return {"success": True}

@monitors_router.get("")
async def get_user_monitors(user_id: int) -> list[Annotated[MonitorSchema, Depends()]]:
    result = await MonitorService.get_user_monitors(user_id)
    return result

@monitors_router.patch("")
async def update_monitor(monitor: Annotated[MonitorChangeSchema, Depends()]):
    await MonitorService.update_monitor(monitor.id, monitor.name, monitor.url)
    return {"success": True}

@monitors_router.delete("")
async def delete_monitor(monitor_id: int):
    await MonitorService.delete_monitor(monitor_id)
    return {"success": True}







