# from agno.vectordb.lancedb.lance_db import LanceDb
from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType

from config import config
from llmx.models import google_embedder, openai_embedder, vllm_embedder

pgvector = PgVector(
    db_url=config.DB_URL,
    table_name="massist_embeddings_0",
    # schema="ai",
    embedder=vllm_embedder,
    search_type=SearchType.vector,
    content_language="russian",
)
