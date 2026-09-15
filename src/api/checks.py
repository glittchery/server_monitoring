from src.api.auth import security
from src.services.check_service import CheckService
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from authx import TokenPayload
from src.api.schemas import CheckSchema, LogsInPeriodSchema

checks_router = APIRouter(
    tags=["Checks API"]
)

@checks_router.post("/checks")
async def perform_check(monitor_id: int, token: TokenPayload = Depends(security.access_token_required)):
    user_id = int(token.sub)
    result = await CheckService.perform_check(monitor_id, user_id)
    if not result["success"]:
        raise HTTPException(status_code=result["status_code"], detail="Not Found")
    return result

@checks_router.get("/monitors/{monitor_id}/checks")
async def get_logs(
        data: Annotated[LogsInPeriodSchema, Depends()],
        token: TokenPayload = Depends(security.access_token_required)
) -> list[CheckSchema]:
    user_id = int(token.sub)
    result = await CheckService.get_logs(data.monitor_id, data.period_start, data.period_end, user_id)
    if not result["success"]:
        raise HTTPException(status_code=result["status_code"], detail="Not Found")
    return result["logs"]

@checks_router.delete("/monitor/{monitor_id}/checks")
async def delete_logs(
        data: Annotated[LogsInPeriodSchema, Depends()],
        token: TokenPayload = Depends(security.access_token_required)
):
    user_id = int(token.sub)
    result = await CheckService.delete_logs(data.monitor_id, data.period_start, data.period_end, user_id)
    if not result["success"]:
        raise HTTPException(status_code=result["status_code"], detail="Not Found")
    return result


