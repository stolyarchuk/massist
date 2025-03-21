from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType

from config import config
from llmx.models import vllm_embedder

pgvector = PgVector(
    db_url=config.DB_URL,
    table_name="massist_embeddings_768",
    # schema="ai",
    embedder=vllm_embedder,
    search_type=SearchType.hybrid,
    content_language="russian",
)
