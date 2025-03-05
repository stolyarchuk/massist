import logging

from agno.agent import Agent
from agno.document.chunking.agentic import AgenticChunking
from agno.embedder.google import GeminiEmbedder
from agno.embedder.huggingface import HuggingfaceCustomEmbedder
from agno.embedder.ollama import OllamaEmbedder
from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.models.deepseek.deepseek import DeepSeek
from agno.models.ollama.chat import Ollama
from agno.models.openai import OpenAIChat
from agno.models.openai.like import OpenAILike
from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.vectordb.lancedb.lance_db import LanceDb
from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType
from openai import OpenAI

from logger import init_module_loggers, update_formatters
from settings import settings

loggers = [logging.getLogger().name]
loggers += list(logging.Logger.manager.loggerDict.keys())

# update_formatters(*loggers)
init_module_loggers(*loggers)

client = OpenAI(
    api_key=settings.OPENAI_API_KEY.get_secret_value(),
    base_url=settings.OPENAI_BASE_URL,
)

models = client.models.list()
model = models.data[0].id

knowledge_base = WebsiteKnowledgeBase(
    urls=[settings.WEBSITE_URL],
    # Number of links to follow from the seed URLs
    max_links=50,
    max_depth=3,
    # Table name: ai.website_documents
    vector_db=PgVector(
        table_name="mdocs_embeddings",
        db_url=settings.DB_URL,
        search_type=SearchType.hybrid,
        embedder=OllamaEmbedder(host=settings.OLLAMA_HOST, dimensions=768),
        # embedder=HuggingfaceCustomEmbedder(api_key=""),
        # embedder=GeminiEmbedder(api_key=settings.GEMINI_API_KEY.get_secret_value()),
    ),
    # vector_db=LanceDb(
    #     table_name="mdocs",
    #     uri="tmp/lancedb",
    #     search_type=SearchType.vector,
    #     # embedder=emb,
    #     # embedder=OllamaEmbedder(
    #     #     id="paraphrase-multilingual",
    #     #     host=settings.OLLAMA_HOST,
    #     # ),
    #     embedder=GeminiEmbedder(api_key=settings.GEMINI_API_KEY.get_secret_value()),
    # ),
    # model=OpenAILike(
    #     id=model,
    #     api_key=settings.OPENAI_API_KEY.get_secret_value(),
    #     base_url=settings.OPENAI_BASE_URL,
    # ),
    chunking_strategy=AgenticChunking(
        model=Ollama(
            id="deepseek-r1:8b",
            host="http://192.168.31.240:11430/",
        ),
        max_chunk_size=1600,
    ),
)

searcher = Agent(
    name="Searcher",
    agent_id="searcher",
    role="Searches for a topic",
    model=Ollama(
        id="deepseek-r1:8b",
        host="http://192.168.31.240:11430/",
    ),
    reasoning=True,
    knowledge=knowledge_base,
    search_knowledge=True,
    read_chat_history=True,
    storage=PostgresAgentStorage(table_name="rag_agent_sessions", db_url=settings.DB_URL),
    instructions=[
        "Always search your knowledge base first and use it if available.",
        "Share the page number or source URL of the information you used in your response.",
        "If health benefits are mentioned, include them in the response.",
        "Important: Use tables where possible.",
    ],
    show_tool_calls=settings.AGENT_SHOW_TOOL_CALLS,
    markdown=settings.AGENT_MARKDOWN,
)

translator = Agent(
    name="Translator",
    agent_id="translator",
    role="Translates from every language to russian",
    model=Ollama(
        id="deepseek-r1:8b",
        host="http://192.168.31.240:11430/",
    ),
    # knowledge=knowledge_base,
    # search_knowledge=True,
    # read_chat_history=True,
    description="You are a senior translator from english to russian. You lived for while in america and that's"
    + "why you know english very well. Given a message in not russian language,"
    + " your goal is to immidiately translate it to russian using all your knowledge of foreign languages.",
    instructions=[
        "Always translate what you hear.",
        "Always answer in russain language.",
        "Be polite",
        "Important: Try not to use harmfull words.",
    ],
    show_tool_calls=settings.AGENT_SHOW_TOOL_CALLS,
    markdown=settings.AGENT_MARKDOWN,
)

manager = Agent(
    team=[searcher, translator],
    description="You are a person who is talking to the outside world. You are listening your team and answer.",
    instructions=[
        "Be interactive. Ask questions if you do not know somethiong",
        "When the silence is too long, tell some random story",
    ],
    reasoning=True,
    model=Ollama(
        id="deepseek-r1:8b",
        host="http://192.168.31.240:11430/",
    ),
    show_tool_calls=settings.AGENT_SHOW_TOOL_CALLS,
    markdown=settings.AGENT_MARKDOWN,
)

app = Playground(agents=[manager]).get_app()

if __name__ == "__main__":

    # Load the knowledge base: Comment after first run as the knowledge base is already loaded
    # knowledge_base.load(upsert=True)
    knowledge_base.load(upsert=True)

    serve_playground_app("agentic_rag_agent_ui:app", reload=True)
