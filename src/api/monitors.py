from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from authx import TokenPayload
from src.api.auth import security
from src.api.schemas import MonitorAddSchema, MonitorSchema, MonitorChangeSchema
from src.services.monitor_service import MonitorService

monitors_router = APIRouter(
    prefix="/monitors",
    tags=["Monitors API"]
)

@monitors_router.post("/create_new")
async def add_monitor(
        monitor: Annotated[MonitorAddSchema, Depends()],
        token: TokenPayload = Depends(security.access_token_required)
):
    user_id = int(token.sub)
    result = await MonitorService.create_monitor(user_id, monitor.type_of_request,
                                                 monitor.name, monitor.url, monitor.interval_minutes)
    return result

@monitors_router.get("/user_monitors")
async def get_user_monitors(
        token: TokenPayload = Depends(security.access_token_required)
):
    user_id = int(token.sub)
    result = await MonitorService.get_user_monitors(user_id)
    return result

@monitors_router.patch("/{monitor_id}")
async def update_monitor(
        monitor: Annotated[MonitorChangeSchema, Depends()],
        token: TokenPayload = Depends(security.access_token_required)
):
    user_id = int(token.sub)
    result = await MonitorService.update_monitor(monitor.id, monitor.name, monitor.url,
                                                 monitor.interval_minutes, user_id)
    if not result["success"]:
        raise HTTPException(status_code=result["status_code"], detail="Not Found")
    return result

@monitors_router.delete("/{monitor_id}")
async def delete_monitor(
        monitor_id: int,
        token: TokenPayload = Depends(security.access_token_required)
):
    user_id = int(token.sub)
    result = await MonitorService.delete_monitor(monitor_id, user_id)
    if not result["success"]:
        raise HTTPException(status_code=result["status_code"], detail="Not Found")
    return result







