from agno.embedder.base import Embedder
from agno.vectordb.base import VectorDb
from agno.vectordb.lancedb.lance_db import LanceDb
from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType

from config import config


def get_vector_db(topic: str, embedder: Embedder) -> VectorDb:
    vector_search_type = config.VECTOR_SEARCH == "vector"
    search_type = SearchType.vector if vector_search_type else SearchType.hybrid

    if config.VECTOR_DB == "pg":
        return PgVector(
            db_url=config.POSTGRES_URL,
            table_name=f"embeddings_{topic}",
            embedder=embedder,
            search_type=search_type,
            content_language="russian",
        )

    if config.VECTOR_DB == "dblance":
        return LanceDb(
            table_name=f"embeddings_{topic}",
            uri=config.DBLANCE_URL,
            search_type=search_type,
            embedder=embedder,
        )

    raise ValueError("bad vector db class name")
