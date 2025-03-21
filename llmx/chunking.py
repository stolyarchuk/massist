from agno.document.chunking.agentic import AgenticChunking

from llmx.models import ds_native, google_model, hf_model, vllm_model

agent_chunking = AgenticChunking(
    model=vllm_model, max_chunk_size=896
)
