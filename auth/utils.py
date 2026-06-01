import bcrypt
from datetime import timezone, datetime, timedelta

import jwt
from env import env


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_jwt(json: dict, key: str, expiry: int) -> str:
    return jwt.encode(
        {
            "claims": json,
            "exp": (datetime.now(timezone.utc) + timedelta(minutes=expiry)).timestamp(),
        },
        key,
        algorithm=env.JWT_ALGORITHM,
    )
