# from agno.vectordb.lancedb.lance_db import LanceDb
from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType

from config import config
from llmx.models import google_embed

pgvector = PgVector(
    db_url=config.DB_URL,
    table_name="massist_embeddings",
    schema="ai",
    embedder=google_embed,
    search_type=SearchType.hybrid,
    content_language="russian",
)
