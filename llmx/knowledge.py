from agno.knowledge.website import WebsiteKnowledgeBase
from agno.models.base import Model

from config import config
from llmx.chunking import get_chunking_strategy
from llmx.logger import logger
from llmx.models import or_mistral_small
from llmx.vector_db import get_vector_db


def get_kb(topic: str, model: Model = or_mistral_small):
    logger.info("Using topic: %s", topic)

    return WebsiteKnowledgeBase(
        urls=[f"{config.WEBSITE_URL}{topic}/"],
        max_links=config.MAX_LINKS,
        max_depth=6,
        vector_db=get_vector_db(topic),
        num_documents=3,
        chunking_strategy=get_chunking_strategy(model)
    )
