import chromadb
from chromadb.api.models.AsyncCollection import AsyncCollection
from env import env


async def get_vector_db() -> AsyncCollection:
    client = await chromadb.AsyncHttpClient(
        host=env.VECTORDB_HOST, port=env.VECTORDB_PORT
    )

    collection = await client.get_or_create_collection("documents")
    return collection
