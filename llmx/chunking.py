from agno.document.chunking.agentic import AgenticChunking
from agno.document.chunking.semantic import SemanticChunking

from llmx.models import google_model

semantic_chunking = SemanticChunking()
agent_chunking = AgenticChunking(
    model=google_model, max_chunk_size=5000
)
