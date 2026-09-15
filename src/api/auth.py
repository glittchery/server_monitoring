from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated
from authx import AuthX, TokenPayload
from src.auth_config import config
from src.api.schemas import UserLoginSchema, UserUpdateSchema
from src.services.auth_service import AuthService
# from src.services.auth_service import

security = AuthX(config=config)

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentification"]
)

@auth_router.post("/register")
async def sign_up(creds: Annotated[UserLoginSchema, Depends()], response: Response):
    if await AuthService.get_user_id(creds.username) is None:
        user_id = await AuthService.insert_user(creds.username, creds.password)
        token = security.create_access_token(uid=str(user_id))
        security.set_access_cookies(token, response)
        return {"success": True}
    raise HTTPException(status_code=409, detail="Username is already taken")

@auth_router.post("/login")
async def sign_in(creds: Annotated[UserLoginSchema, Depends()], response: Response):
    result = await AuthService.log_in(creds.username, creds.password)
    if result["success"]:
        token = security.create_access_token(uid=str(result["user_id"]))
        security.set_access_cookies(token, response)
        return {"success": True}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@auth_router.patch("/account")
async def change_credentials(
        new_creds: Annotated[UserUpdateSchema, Depends()],
        token: TokenPayload = Depends(security.access_token_required)
):
    user_id = int(token.sub)
    await AuthService.update_user(user_id, new_creds.new_username, new_creds.new_password)
    return {"success": True}

@auth_router.delete("/account")
async def delete_account(
        token: TokenPayload = Depends(security.access_token_required)
):
    user_id = int(token.sub)
    await AuthService.delete_user(user_id)
    return {"success": True}






