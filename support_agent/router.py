from chromadb.api.models.AsyncCollection import AsyncCollection
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from sqlalchemy.ext.asyncio import AsyncSession
from auth.dependencies import verify_access_token, get_current_user

from models.employee import Employee

from db.connection import get_db
from db.vector_connection import get_vector_db
from db.checkpointer import get_checkpointer

from support_agent import service
from support_agent.schema import PromptRequest

support_agent_router = APIRouter(
    prefix="/support-agent",
    tags=["Support Agent"],
    dependencies=[Depends(verify_access_token)],
)


@support_agent_router.post("/chat")
async def prompt_support_agent(
    body: PromptRequest,
    db: AsyncSession = Depends(get_db),
    vec_db: AsyncCollection = Depends(get_vector_db),
    checkpointer: AsyncPostgresSaver = Depends(get_checkpointer),
    current_user: Employee = Depends(get_current_user),
):
    return StreamingResponse(
        service.invoke_agent(
            thread_id=f"E-{current_user.id}",
            prompt=body.prompt,
            checkpointer=checkpointer,
            db=db,
            vec_db=vec_db,
        ),
        media_type="text/event-stream",
    )
