from pydantic import BaseModel
from pydantic.config import ConfigDict

class TokenResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    token_type: str
    access_token: str
    refresh_token: str
