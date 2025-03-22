from agno.document.chunking.agentic import AgenticChunking

from llmx.models import google_model, vllm_model


def get_agent_chanking(max_chank: int):
    return AgenticChunking(
        model=google_model, max_chunk_size=max_chank
    )
