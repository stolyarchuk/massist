from agno.knowledge.website import WebsiteKnowledgeBase

from config import config
from llmx.chunking import get_agent_chanking
from llmx.vectordb import get_vectordb


def get_kb(num: int):
    return WebsiteKnowledgeBase(
        urls=[config.WEBSITE_URL],
        max_links=config.MAX_LINKS,
        max_depth=6,
        vector_db=get_vectordb(num),
        num_documents=3,
        chunking_strategy=get_agent_chanking(num)
    )
