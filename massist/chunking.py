from agno.document.chunking.agentic import AgenticChunking
from agno.document.chunking.document import DocumentChunking
from agno.document.chunking.recursive import RecursiveChunking
from agno.document.chunking.semantic import SemanticChunking
from agno.document.chunking.strategy import ChunkingStrategy
from agno.models.base import Model

from config import config
from massist.models import get_openai_embedder


def get_chunking_strategy(model: Model, max_chunk_size: int = config.MAX_CHUNK_SIZE) -> ChunkingStrategy:
    if config.CHUNKING_STRATEGY == "agentic":
        return AgenticChunking(model=model, max_chunk_size=max_chunk_size)

    if config.CHUNKING_STRATEGY == "recursive":
        return RecursiveChunking(chunk_size=max_chunk_size)

    if config.CHUNKING_STRATEGY == "document":
        return DocumentChunking(chunk_size=max_chunk_size)

    if config.CHUNKING_STRATEGY == "semantic":
        return SemanticChunking(
            embedder=get_openai_embedder(),
            chunk_size=max_chunk_size
        )

    raise ValueError("bad chunking strategy")
