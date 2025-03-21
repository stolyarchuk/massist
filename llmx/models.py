from agno.embedder.google import GeminiEmbedder
from agno.embedder.openai import OpenAIEmbedder
from agno.models.deepseek.deepseek import DeepSeek
from agno.models.google.gemini import Gemini
from agno.models.huggingface.huggingface import HuggingFace
from agno.models.openai.like import OpenAILike

from config import config  # Local import

hf_model = HuggingFace(
    id="mistralai/Mistral-Small-3.1-24B-Instruct-2503", max_tokens=65536, api_key=config.HUGGINGFACE_API_KEY
)

ds_native = DeepSeek(
    id="deepseek-chat", max_tokens=65536, api_key=config.DEEPSEEK_API_KEY
)

ds_model = HuggingFace(
    id="deepseek-ai/DeepSeek-R1", max_tokens=65536, api_key=config.HUGGINGFACE_API_KEY
)

google_model = Gemini(api_key=config.GOOGLE_API_KEY)


massist_memory_model = OpenAILike(
    id="google/gemini-2.0-flash-lite-preview-02-05:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=config.OPENROUTER_API_KEY,
)

hf_model_or = OpenAILike(
    id="mistralai/mistral-small-3.1-24b-instruct:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=config.OPENROUTER_API_KEY,
)


deepseek_model = OpenAILike(
    id="deepseek/deepseek-r1:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=config.OPENROUTER_API_KEY,
)


google_embedder = GeminiEmbedder(
    api_key=config.GOOGLE_API_KEY,
    id="text-multilingual-embedding-002",
    # dimensions=1536,
)

vllm_model = OpenAILike(
    id="neuralmagic/DeepSeek-R1-Distill-Qwen-7B-quantized.w4a16",
    base_url="http://192.168.31.240:8000/v1",
    api_key="sk-d00b792327b44da6876a1419e059ee99"
)

vllm_embedder = OpenAIEmbedder(
    id="BAAI/bge-m3",
    dimensions=1024,
    base_url="http://192.168.31.240:8001/v1",
    api_key="sk-d00b792327b44da6876a1419e059ee99"
)
