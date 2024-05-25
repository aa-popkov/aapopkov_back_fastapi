from datetime import timedelta, datetime

import bcrypt
import jwt

from utils.config import config


def encode_jwt(
    payload: dict,
    private_key: str = config.JWT.private_key.read_text(),
    algorithm: str = config.JWT.algorithm,
    expire_minutes: int = config.JWT.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    """
    Encode JWT payload to JWT string
    :param payload: JWT payload
    :param private_key: Private key RSA256
    :param algorithm: JWT algorithm
    :param expire_minutes: Expire time in minutes
    :param expire_timedelta: Expire time in minutes
    :return: Encoded JWT string
    """
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = config.JWT.public_key.read_text(),
    algorithm: str = config.JWT.algorithm,
) -> dict:
    decoded: dict = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
