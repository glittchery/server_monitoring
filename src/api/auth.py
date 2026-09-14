from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated
from authx import AuthX
from src.auth_config import config
from src.api.schemas import UserLoginSchema
from src.services.auth_service import AuthService
# from src.services.auth_service import

security = AuthX(config=config)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentification"]
)

@auth_router.post("/sign_up")
async def sign_up(creds: UserLoginSchema, response: Response):
    if AuthService.get_user_id(creds.username) is None:
        user_id = await AuthService.insert_user(creds.username, creds.password)
        token = security.create_access_token(uid=str(user_id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=409, detail="Username is already taken")

@auth_router.post("/sign_in")
async def sign_in(creds: UserLoginSchema, response: Response):
    result = await AuthService.log_in(creds.username, creds.password)["success"]
    if result["success"]:
        token = security.create_access_token(uid=str(result["user_id"]))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")




