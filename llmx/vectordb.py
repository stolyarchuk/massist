from agno.embedder.base import Embedder
from agno.vectordb.base import VectorDb
from agno.vectordb.lancedb.lance_db import LanceDb
from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType

from config import config
from llmx.models import vllm_embedder


def get_vectordb(name: str = "lance", size: int = 1024, embedder: Embedder = vllm_embedder) -> VectorDb:
    if name == "pg":
        return PgVector(
            db_url=config.DB_URL,
            table_name=f"massist_embeddings_{size}",
            embedder=embedder,
            search_type=SearchType.vector,
            content_language="russian",
        )

    if name == "lance":
        return LanceDb(
            table_name=f"massist_embeddings_{size}",
            uri="tmp/lancedb",
            search_type=SearchType.vector,
            embedder=embedder,
        )

    raise ValueError("bad vector db class name")
