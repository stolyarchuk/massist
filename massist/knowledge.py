from agno.knowledge.website import WebsiteKnowledgeBase
from agno.models.base import Model

from config import config
from massist.chunking import get_chunking_strategy
from massist.logger import get_logger
from massist.models import get_google_embedder, get_openai_embedder, get_vllm_embedder
from massist.vector_db import get_vector_db

logger = get_logger(__name__)


def get_kb(
    topic: str,
    chunking_model: Model,
    max_links: int = config.MAX_LINKS,
    max_depth: int = config.MAX_DEPTH,
):
    url = (
        f"{config.WEBSITE_URL}{topic}.html"
        if topic == "index"
        else f"{config.WEBSITE_URL}{topic}/"
    )

    if config.VECTOR_EMBEDDER == "vllm":
        embedder = get_vllm_embedder()
    elif config.VECTOR_EMBEDDER == "google":
        embedder = get_google_embedder()
    elif config.VECTOR_EMBEDDER == "openai":
        embedder = get_openai_embedder()
    else:
        raise ValueError(f"Unknown vector embedder: {config.VECTOR_EMBEDDER}")

    kb = WebsiteKnowledgeBase(
        urls=[url],
        max_links=max_links,
        max_depth=max_depth,
        bad_fragment="",
        bad_path="mitigator.ova",
        base_url=url,
        vector_db=get_vector_db(topic, embedder),
        num_documents=3,
        chunking_strategy=get_chunking_strategy(chunking_model),
    )

    logger.debug("Loaded KB: %s. (source: %s)", kb, url)
    return kb
