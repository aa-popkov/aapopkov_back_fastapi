from fastapi import APIRouter, Depends

from api_v1.depends.user import validate_user, get_current_active_user
from schemas.jwt import Token
from schemas.user import UserSchema
from utils import auth

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(user: UserSchema = Depends(validate_user)):
    jwt_payload = {
        "sub": user.username,
    }

    token = auth.encode_jwt(jwt_payload)

    return Token(access_token=token, token_type="Bearer")


@router.get("/info")
async def info(user: UserSchema = Depends(get_current_active_user)):
    return user
