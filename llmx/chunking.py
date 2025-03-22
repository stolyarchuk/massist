from agno.document.chunking.agentic import AgenticChunking

from llmx.models import google_model, mistral_model, openai_model, vllm_model


def get_agent_chanking(chunk_size: int):
    return AgenticChunking(
        model=mistral_model, max_chunk_size=chunk_size
    )
