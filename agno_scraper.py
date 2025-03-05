from agno.agent.agent import Agent

# from agno.embedder.google import GeminiEmbedder
from agno.document.chunking.agentic import AgenticChunking
from agno.embedder.ollama import OllamaEmbedder
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.models.deepseek.deepseek import DeepSeek
from agno.models.openai.like import OpenAILike
from agno.vectordb.pgvector.pgvector import PgVector

from settings import Settings

settings = Settings()

knowledge_base = WebsiteKnowledgeBase(
    urls=[settings.WEBSITE_URL],
    # Number of links to follow from the seed URLs
    max_links=10,
    max_depth=3,
    # Table name: ai.website_documents
    vector_db=PgVector(
        table_name="mdocs_embeddings",
        db_url=settings.DB_URL,
        embedder=OllamaEmbedder(dimensions=4096),
    ),
    chunking_strategy=AgenticChunking(
        model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value()), max_chunk_size=2048
    ),
)


agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
)

agent.knowledge.load(recreate=False)
