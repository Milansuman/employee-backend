from pydantic import BaseModel


class LoginAttempt(BaseModel):
    email: str
    password: str
