from chromadb.api.models.AsyncCollection import AsyncCollection
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.document import Document


async def get_documents(employee_id: int, db: AsyncSession):
    documents = await db.scalars(
        select(Document)
        .options(selectinload(Document.employee))
        .where(Document.employee_id == employee_id)
        .where(Document.deleted_at.is_(None))
    )

    return list(documents)


async def get_document_chunks(filename: str, vec_db: AsyncCollection):
    chunks = await vec_db.query(where={"source": filename})

    if chunks["documents"] is None:
        raise AttributeError("Documents is none")

    return "\n".join([chunk for chunk in chunks["documents"][0]])


async def query_document(
    query_embedding: list[float], vec_db: AsyncCollection, top_k: int = 10
):
    chunks = await vec_db.query(query_embeddings=[query_embedding], n_results=top_k)

    return chunks


async def add_document(employee_id: int, filename: str, mime: str, db: AsyncSession):
    document = Document(filename=filename, mime=mime, employee_id=employee_id)

    db.add(document)
    await db.commit()

    return document


async def add_chunks(
    filename: str,
    embeddings: list[list[float]],
    chunks: list[str],
    vec_db: AsyncCollection,
):
    await vec_db.add(
        ids=[f"{filename}_chunk_{i}" for i, _ in enumerate(chunks)],
        documents=chunks,
        embeddings=[*embeddings],
        metadatas=[{"source": filename} for _ in chunks],
    )
