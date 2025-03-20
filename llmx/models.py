from agno.embedder.google import GeminiEmbedder
from agno.embedder.openai import OpenAIEmbedder
from agno.models.google.gemini import Gemini
from agno.models.openai.like import OpenAILike
from agno.models.openrouter.openrouter import OpenRouter

from config import config  # Local import

google_model = Gemini(api_key=config.GOOGLE_API_KEY)

google_embed = GeminiEmbedder(
    api_key=config.GOOGLE_API_KEY,
    id=config.GEMINI_EMBED_MODEL,
    dimensions=1536,
)

massist_memory_model_vllm = OpenAILike(
    id="neuralmagic/Qwen2-0.5B-Instruct-quantized.w8a8",
    base_url="http://192.168.31.240:8000/v1",
    api_key="sk-d00b792327b44da6876a1419e059ee99",
    max_tokens=32768
)


massist_memory_model = OpenAILike(
    id="google/gemini-2.0-flash-lite-preview-02-05:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=config.OPENROUTER_API_KEY,
)


vllm_embedder = OpenAIEmbedder(
    id="BAAI/bge-m3",
    dimensions=1024,
    base_url="http://192.168.31.240:8000/v1",
    api_key="sk-d00b792327b44da6876a1419e059ee99"
)
