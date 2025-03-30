from agno.embedder.google import GeminiEmbedder
from agno.embedder.openai import OpenAIEmbedder
# from agno.models.deepseek.deepseek import DeepSeek
from agno.models.google.gemini import Gemini
# from agno.models.huggingface.huggingface import HuggingFace
from agno.models.openai.like import OpenAILike

from config import config  # Local import

# openai_model = OpenAIChat(api_key=config.OPENAI_API_KEY)

# hf_model = HuggingFace(
#     id="mistralai/Mistral-Small-3.1-24B-Instruct-2503", max_tokens=65536, api_key=config.HUGGINGFACE_API_KEY
# )

# ds_deepseek_r1 = DeepSeek(
#     id="deepseek-chat", max_tokens=65536, api_key=config.DEEPSEEK_API_KEY
# )

# hf_deepseek_r1 = HuggingFace(
#     id="deepseek-ai/DeepSeek-R1", max_tokens=65536, api_key=config.HUGGINGFACE_API_KEY
# )


def get_google_model(
    model_id: str = config.GEMINI_MODEL_PRI,
    temperature: float = config.TEMPERATURE
):
    return Gemini(
        id=model_id,
        api_key=config.GOOGLE_API_KEY,
        temperature=temperature
    )


def get_openrouter_model(
    base_url: str = "https://openrouter.ai/api/v1",
    model_id: str = config.OPENROUTER_MODEL,
    temperature: float = config.TEMPERATURE
):
    return OpenAILike(
        id=model_id,
        base_url=base_url,
        api_key=config.OPENROUTER_API_KEY,
        temperature=temperature
    )


def get_mistral_model(temperature: float = config.TEMPERATURE):
    return get_openrouter_model(
        model_id="mistralai/mistral-small-3.1-24b-instruct:free",
        temperature=temperature
    )


def get_gemini_pri_model(temperature: float = config.TEMPERATURE):
    return get_google_model(model_id=config.GEMINI_MODEL_PRI, temperature=temperature)


def get_gemini_sub_model(temperature: float = config.TEMPERATURE):
    return get_google_model(model_id=config.GEMINI_MODEL_SEC, temperature=temperature)

# or_gemini2_flash = OpenAILike(
#     id="google/gemini-2.0-flash-lite-preview-02-05:free",
#     base_url="https://openrouter.ai/api/v1",
#     api_key=config.OPENROUTER_API_KEY,
#     temperature=config.TEMPERATURE
# )


# or_deepseek_r1 = OpenAILike(
#     id="deepseek/deepseek-r1:free",
#     base_url="https://openrouter.ai/api/v1",
#     api_key=config.OPENROUTER_API_KEY,
# )

# google_embedder = GeminiEmbedder(
#     api_key=config.GOOGLE_API_KEY,
#     id=config.GEMINI_EMBED_MODEL,
#     dimensions=3072,
# )

def get_vllm_model(base_url: str = config.VLLM_BASE_URL_PRI, model_id: str = config.VLLM_MODEL, ):
    return OpenAILike(
        id=model_id,
        base_url=base_url,
        api_key=config.VLLM_API_KEY,
        # max_tokens=32768,
    )


def get_vllm_embedder(base_url: str = config.VLLM_BASE_URL_PRI, model_id: str = "BAAI/bge-m3", dims: int = config.DIMS):
    return OpenAIEmbedder(
        id=model_id,
        dimensions=dims,
        base_url=base_url,
        api_key=config.VLLM_API_KEY
    )
