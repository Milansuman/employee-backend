import bcrypt
from fastapi import Cookie
from datetime import timezone, datetime, timedelta

from jwt.exceptions import DecodeError

from exceptions import UnauthorizedException
import jwt
from env import env

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def create_jwt(json: dict, key: str, expiry: int) -> str:
    return jwt.encode({
        "claims": json,
        "exp": (datetime.now(timezone.utc) + timedelta(minutes=expiry)).timestamp()
    }, key, algorithm=env.JWT_ALGORITHM)

def verify_access_token(access: str | None = Cookie(default=None)):
    if not access:
        raise UnauthorizedException("Employee has not logged in")

    try:
        claims = jwt.decode(access, env.JWT_SECRET, algorithms=[env.JWT_ALGORITHM])

        if claims["exp"] < datetime.now(timezone.utc).timestamp():
            raise UnauthorizedException("Token expired")

    except DecodeError:
        raise UnauthorizedException("Invalid token")
