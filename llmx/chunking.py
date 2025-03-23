from agno.document.chunking.agentic import AgenticChunking
from agno.document.chunking.strategy import ChunkingStrategy
from agno.models.base import Model

from config import config


def get_agent_chanking(model: Model) -> ChunkingStrategy:
    return AgenticChunking(model=model, max_chunk_size=config.DIMENSIONS)
