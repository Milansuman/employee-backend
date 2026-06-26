from pydantic import BaseModel
from dataclasses import dataclass
from chromadb.api.models.AsyncCollection import AsyncCollection
from sqlalchemy.ext.asyncio import AsyncSession


class PromptRequest(BaseModel):
    prompt: str


@dataclass
class RuntimeContext:
    db: AsyncSession
    vec_db: AsyncCollection
