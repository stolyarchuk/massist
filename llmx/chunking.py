from agno.document.chunking.agentic import AgenticChunking
# from agno.document.chunking.semantic import SemanticChunking
from dotenv import load_dotenv

from llmx.models import ds_native, google_model, hf_model, vllm_model

load_dotenv()


# semantic_chunking = SemanticChunking()

agent_chunking = AgenticChunking(
    model=ds_native, max_chunk_size=1024
)
