from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated
from authx import AuthX
from src.auth_config import config
from src.api.schemas import UserLoginSchema, UserUpdateSchema
from src.services.auth_service import AuthService
# from src.services.auth_service import

security = AuthX(config=config)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentification"]
)

@auth_router.post("/sign_up")
async def sign_up(creds: Annotated[UserLoginSchema, Depends()], response: Response):
    if await AuthService.get_user_id(creds.username) is None:
        user_id = await AuthService.insert_user(creds.username, creds.password)
        token = security.create_access_token(uid=str(user_id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=409, detail="Username is already taken")

@auth_router.post("/sign_in")
async def sign_in(creds: Annotated[UserLoginSchema, Depends()], response: Response):
    result = await AuthService.log_in(creds.username, creds.password)["success"]
    if result["success"]:
        token = security.create_access_token(uid=str(result["user_id"]))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@auth_router.patch("/change_credentials")
async def change_credentials(
        new_creds: Annotated[UserUpdateSchema, Depends()],
        token=Depends(security.access_token_required)
):
    user_id = token.sub
    await AuthService.update_user(user_id, new_creds.new_username, new_creds.new_password)
    return {"success": True}

@auth_router.patch("/delete_account")
async def delete_account(
        token=Depends(security.access_token_required)
):
    user_id = token.sub
    await AuthService.delete_user(user_id)
    return {"success": True}






