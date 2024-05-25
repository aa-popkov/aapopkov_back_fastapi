from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    hashed_password: bytes
    is_active: bool
    is_superuser: bool
