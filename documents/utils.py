from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


def chunk_markdown(
    markdown: str, chunk_size: int = 500, chunk_overlap: int = 100
) -> list[str]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    return text_splitter.split_text(markdown)


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)

    return embeddings.tolist()
