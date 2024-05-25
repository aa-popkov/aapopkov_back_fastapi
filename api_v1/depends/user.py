from fastapi import Form, HTTPException, Depends
from starlette import status

import utils.auth
from api_v1.depends.jwt import get_current_token_payload
from models.user import User
from schemas.user import UserSchema


async def validate_user(username: str = Form(), password: str = Form()):
    exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
    )
    user = await User.get_by_username(username.lower().strip())
    if not user:
        raise exp

    if not utils.auth.validate_password(password, user.hashed_password):
        raise exp

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    return user


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username = payload.get("sub")
    user = await User.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid"
        )
    return UserSchema(**user.__dict__)


def get_current_active_user(user: UserSchema = Depends(get_current_auth_user)):
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )
    return user


def check_is_admin(user: UserSchema = Depends(get_current_active_user)) -> UserSchema:
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not have permission to perform this action",
        )
    return user
