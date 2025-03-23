from agno.document.chunking.agentic import AgenticChunking
from agno.models.base import Model

from llmx.models import mistral_model


def get_agent_chanking(chunk_size: int = 1024, model: Model = mistral_model):
    return AgenticChunking(
        model=mistral_model, max_chunk_size=chunk_size
    )
