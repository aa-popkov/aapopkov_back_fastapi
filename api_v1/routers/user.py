from typing import List

from fastapi import APIRouter, HTTPException, status, Depends, Form, Query

from models.user import User
from api_v1.depends.user import check_is_admin, get_current_active_user
from schemas.user import UserSchema
from utils.auth import hash_password

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", description="Create new User", dependencies=[Depends(check_is_admin)])
async def create_user(
    username: str = Form(min_length=3, max_length=25),
    password: str = Form(min_length=8),
    is_active: bool = Form(default=True),
    is_superuser: bool = Form(default=False),
):
    username = username.lower().strip()
    check_user = await User.get_by_username(username)
    if check_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists!"
        )
    pwd_hash = hash_password(password)
    user_model = User(
        username=username,
        hashed_password=pwd_hash,
        is_active=is_active,
        is_superuser=is_superuser,
    )
    user = await User.create(user_model)
    return user


@router.delete("/", description="Delete existing User")
async def delete_user(
    username: str = Form(), user: UserSchema = Depends(check_is_admin)
):
    username = username.lower().strip()
    if user.username == username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can't delete your self!"
        )
    check_user = await User.get_by_username(username)
    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    deleted_user = await User.delete_by_username(username)
    return "Ok"


@router.post("/change_password", description="Change password")
async def change_password(
    new_password: str = Form(min_length=8),
    user: UserSchema = Depends(get_current_active_user),
):
    new_password = hash_password(new_password)
    if new_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The new password is equal to the old password!",
        )
    user_model = await User.get_by_username(user.username)
    await User.change_password(user_model, new_password)
    return "Ok"


@router.get(
    "/get_all", response_model=List[UserSchema], dependencies=[Depends(check_is_admin)]
)
async def get_all_users(page_number: int = Query(default=0), page_size: int = Query(default=10, le=50)):
    model_users = await User.get_all_users(page_number*page_size, page_size)
    schema_users = [UserSchema(
        username=x.username,
        hashed_password=x.hashed_password,
        is_active=x.is_active,
        is_superuser=x.is_superuser
    ) for x in model_users]
    return schema_users
