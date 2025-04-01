from agno.knowledge.website import WebsiteKnowledgeBase
from agno.models.base import Model

from config import config
from massist.chunking import get_chunking_strategy
from massist.logger import logger
from massist.models import get_vllm_embedder
from massist.vector_db import get_vector_db


def get_kb(
    topic: str,
    model: Model,
    max_links: int = config.MAX_LINKS,
    max_depth: int = config.MAX_DEPTH
):
    url = f"{config.WEBSITE_URL}{topic}.html" if topic == "index" else f"{config.WEBSITE_URL}{topic}/"
    logger.info("Using topic: %s, url: %s", topic, url)

    return WebsiteKnowledgeBase(
        urls=[url],
        max_links=max_links,
        max_depth=max_depth,
        vector_db=get_vector_db(topic, get_vllm_embedder()),
        num_documents=3,
        chunking_strategy=get_chunking_strategy(model)
    )
