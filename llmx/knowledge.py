from agno.knowledge.website import WebsiteKnowledgeBase

from config import config
from llmx.chunking import agent_chunking
from llmx.vectordb import pgvector

knowledge_base = WebsiteKnowledgeBase(
    urls=[config.WEBSITE_URL],
    max_links=config.MAX_LINKS,
    max_depth=6,
    vector_db=pgvector,
    # optimize_on=5000,
    num_documents=3,
    chunking_strategy=agent_chunking
)
