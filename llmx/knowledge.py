from agno.knowledge.website import WebsiteKnowledgeBase
from agno.models.base import Model

from config import config
from llmx.chunking import get_agent_chanking
from llmx.logger import logger
from llmx.models import mistral_model
from llmx.vectordb import get_vectordb


def get_kb(topic: str, model: Model = mistral_model):
    logger.info("Using topic: %s", topic)

    return WebsiteKnowledgeBase(
        urls=[f"{config.WEBSITE_URL}{topic}/"],
        max_links=config.MAX_LINKS,
        max_depth=6,
        vector_db=get_vectordb(topic),
        num_documents=3,
        chunking_strategy=get_agent_chanking(model)
    )
