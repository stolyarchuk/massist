from agno.embedder.base import Embedder
from agno.vectordb.base import VectorDb
from agno.vectordb.lancedb.lance_db import LanceDb
from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType

from config import config


def get_vector_db(topic: str, embedder: Embedder) -> VectorDb:
    if config.VECTOR_DB == "pg":
        return PgVector(
            db_url=config.POSTGRES_URL,
            table_name=f"embeddings_{topic}",
            embedder=embedder,
            search_type=SearchType.vector,
            content_language="russian"
        )

    if config.VECTOR_DB == "dblance":
        return LanceDb(
            table_name=f"embeddings_{topic}",
            uri="tmp/dblance",
            search_type=SearchType.vector,
            embedder=embedder,
        )

    raise ValueError("bad vector db class name")
