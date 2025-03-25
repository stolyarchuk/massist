from agno.embedder.base import Embedder
from agno.vectordb.base import VectorDb
from agno.vectordb.lancedb.lance_db import LanceDb
from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType

from config import config
from llmx.models import vllm_embedder


def get_vector_db(topic: str = "index", embedder: Embedder = vllm_embedder) -> VectorDb:
    if config.VECTOR_DB == "pg":
        return PgVector(
            db_url=config.POSTGRES_URL,
            table_name=f"embeddings_{topic}",
            embedder=embedder,
            search_type=SearchType.hybrid,
            content_language="russian",
        )

    if config.VECTOR_DB == "lance":
        return LanceDb(
            table_name=f"embeddings_{topic}",
            uri="tmp/lancedb",
            search_type=SearchType.vector,
            embedder=embedder,
        )

    raise ValueError("bad vector db class name")
