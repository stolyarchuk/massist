from agno.embedder.base import Embedder
from agno.vectordb.base import VectorDb
from agno.vectordb.lancedb.lance_db import LanceDb
from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType

from config import config
from massist.logger import get_logger

logger = get_logger(__name__)


def get_vector_db(topic: str, embedder: Embedder) -> VectorDb:
    # Convert string to enum value
    try:
        search_type = SearchType[config.VECTOR_SEARCH.lower()]
    except KeyError:
        # Default to vector search if string doesn't match any enum value
        search_type = SearchType.vector

    logger.debug(f"Using search_type: {search_type}")

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
