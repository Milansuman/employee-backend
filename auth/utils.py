import bcrypt
from fastapi import Cookie

from exceptions import UnauthorizedException
import jwt
from env import env

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def verify_access_token(auth: str | None = Cookie(default=None)):
    if not auth:
        raise UnauthorizedException("Employee has not logged in")

    try:
        jwt.decode(auth, env.JWT_SECRET, algorithms=["HS256"])
    except Exception:
        raise UnauthorizedException("Invalid token")
