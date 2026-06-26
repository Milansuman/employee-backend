from chromadb.api.models.AsyncCollection import AsyncCollection
from sqlalchemy.ext.asyncio import AsyncSession
from markitdown import MarkItDown
from io import BytesIO

from documents import repository, utils


async def get_documents(
    employee_id: int,
    db: AsyncSession,
):
    try:
        documents = await repository.get_documents(employee_id=employee_id, db=db)

        return documents
    except Exception as e:
        raise e


async def add_document(
    employee_id: int,
    filename: str,
    mime: str,
    content: bytes,
    db: AsyncSession,
    vec_db: AsyncCollection,
):
    try:
        await repository.add_document(
            employee_id=employee_id, filename=filename, mime=mime, db=db
        )

        parser = MarkItDown()
        md_content = parser.convert(BytesIO(content)).markdown

        chunks = utils.chunk_markdown(md_content)

        embeddings = utils.embed_chunks(chunks)

        await repository.add_chunks(
            chunks=chunks, embeddings=embeddings, filename=filename, vec_db=vec_db
        )
    except Exception as e:
        raise e
