from collections.abc import AsyncGenerator
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from env import env


async def setup_checkpointer():
    async with AsyncPostgresSaver.from_conn_string(
        conn_string=env.CHECKPOINTER_URL
    ) as checkpointer_connection:
        await checkpointer_connection.setup()


async def get_checkpointer() -> AsyncGenerator[AsyncPostgresSaver, None]:
    async with AsyncPostgresSaver.from_conn_string(
        conn_string=env.CHECKPOINTER_URL
    ) as checkpointer_connection:
        yield checkpointer_connection
