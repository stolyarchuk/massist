from agno.vectordb.lancedb.lance_db import LanceDb
from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType

from config import config
from llmx.models import vllm_embedder

pgvector = PgVector(
    db_url=config.DB_URL,
    table_name="massist_embeddings_1024",
    # schema="ai",
    embedder=vllm_embedder,
    search_type=SearchType.vector,
    content_language="russian",
)


def get_vectordb(size: int):
    return LanceDb(
        table_name=f"massist_embeddings_{size}",
        uri="tmp/lancedb",
        search_type=SearchType.vector,
        embedder=vllm_embedder
    )
