import json

from chromadb.api.models.AsyncCollection import AsyncCollection
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from sqlalchemy.ext.asyncio import AsyncSession

from support_agent.agent import RuntimeContext, get_agent


async def invoke_agent(
    thread_id: str | None,
    prompt: str,
    db: AsyncSession,
    vec_db: AsyncCollection,
    checkpointer: AsyncPostgresSaver,
):
    agent = get_agent(checkpointer=checkpointer)

    stream = agent.astream(
        {"messages": [HumanMessage(content=prompt)]},
        config={"configurable": {"thread_id": thread_id}},
        context=RuntimeContext(db=db, vec_db=vec_db),
        stream_mode="messages",
        version="v2",
    )

    async for chunk in stream:
        if chunk["type"] == "messages":
            token, metadata = chunk["data"]

            if (
                len(token.content_blocks) > 0
                and token.content_blocks[0]["type"] == "text"
            ):
                yield f"data: {
                    json.dumps({'content': token.content_blocks[0]['text']})
                }\n\n"

    yield "data: [DONE]\n\n"
