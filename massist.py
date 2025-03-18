# Standard library imports
import logging
import sys

from agno.agent.agent import Agent
from agno.document.chunking.agentic import AgenticChunking
from agno.document.chunking.semantic import SemanticChunking
# from agno.embedder.fastembed import FastEmbedEmbedder
# from agno.document.reader.firecrawl_reader import FirecrawlReader  # Unused import
# from agno.embedder.cohere import CohereEmbedder  # Unused import
from agno.embedder.google import GeminiEmbedder
from agno.embedder.huggingface import HuggingfaceCustomEmbedder
from agno.embedder.ollama import OllamaEmbedder  # Unused import
from agno.embedder.openai import OpenAIEmbedder
# from agno.knowledge.document import DocumentKnowledgeBase  # Unused import
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.memory.agent import AgentMemory
from agno.memory.classifier import MemoryClassifier
from agno.memory.db.postgres import PgMemoryDb
from agno.memory.manager import MemoryManager
from agno.memory.summarizer import MemorySummarizer
# from agno.models.deepseek.deepseek import DeepSeek  # Unused import
from agno.models.google.gemini import Gemini
from agno.models.ollama.chat import Ollama  # Unused import
# Agno imports
from agno.models.openai.like import OpenAILike
# from agno.models.ollama.tools import OllamaTools  # Unused import
# from agno.models.openai.chat import OpenAIChat  # Unused import
# from agno.models.openrouter.openrouter import OpenRouter  # Unused import
# from agno.models.openai.like import OpenAILike
from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app
# from agno.reranker.base import Reranker  # Unused import
# from agno.reranker.cohere import CohereReranker  # Unused import
from agno.storage.postgres import PostgresStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.utils.log import logger
# from agno.vectordb.lancedb.lance_db import LanceDb
from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType
from agno.workflow.workflow import Workflow
# Third-party imports
from dotenv import load_dotenv
from ollama import Client as OllamaClient

# Local imports
from logger import init_module_loggers, update_formatters
from settings import settings

load_dotenv()
# loggers = [logging.getLogger().name]
# loggers += list(logging.Logger.manager.loggerDict.keys())

loggers = [lgr for lgr in logging.Logger.manager.loggerDict.keys()]

# update_formatters(*loggers)
init_module_loggers(*loggers)

google_embed = GeminiEmbedder(
    api_key=settings.GOOGLE_API_KEY,
    id=settings.GEMINI_EMBED_MODEL,
    dimensions=768,
)

# ollama0_model = Ollama(id="gemma3:4b", host=settings.OLLAMA0_HOST)
# ollama1_model = Ollama(id="gemma3:1b", host=settings.OLLAMA1_HOST)

# ollama_embed = OllamaEmbedder(
#     id="paraphrase-multilingual", dimensions=768, host=settings.OLLAMA1_HOST
# )

mlinks = ['https://docs.mitigator.ru/v24.10/',
          'https://docs.mitigator.ru/v24.10/install/',
          'https://docs.mitigator.ru/v24.10/maintenance/']

mindex = 1

knowledge_base = WebsiteKnowledgeBase(
    urls=[mlinks[mindex]],
    max_links=500,
    max_depth=4,
    vector_db=PgVector(
        db_url=settings.DB_URL,
        table_name=f"massist_embeddings_{mindex}",
        schema="ai",
        embedder=google_embed,
        search_type=SearchType.hybrid,
        content_language="russian",
    ),
    # optimize_on=5000,
    num_documents=5,
    chunking_strategy=AgenticChunking(
        model=Gemini(api_key=settings.GOOGLE_API_KEY), max_chunk_size=3000
    ),
    # chunking_strategy=SemanticChunking(OpenAIEmbedder(chunk_size=5000),
)

massist_memory_model = OpenAILike(
    id="google/gemini-2.0-flash-lite-preview-02-05:free",
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY,
)

# massist_memory_model_vllm = OpenAILike(
#     id="neuralmagic/Qwen2-0.5B-Instruct-quantized.w8a8",
#     base_url="http://192.168.31.240:8000/v1",
#     api_key="sk-d00b792327b44da6876a1419e059ee99",
#     max_tokens=32768
# )


massist_memory = AgentMemory(
    # Persist memory in Postgres
    user_id="stolyarchuk",
    db=PgMemoryDb(table_name="massist_memory", db_url=settings.DB_URL),
    create_user_memories=True,
    update_user_memories_after_run=True,
    create_session_summary=True,
    update_session_summary_after_run=True,
    manager=MemoryManager(model=massist_memory_model),
    classifier=MemoryClassifier(model=massist_memory_model),
    summarizer=MemorySummarizer(model=massist_memory_model),
)

massist_storage = PostgresStorage(
    table_name="massist_sessions", db_url=settings.DB_URL
)

mitigator_assistant = Agent(
    name="Mitigator Assistant",
    agent_id="mitigator_assistant",
    session_id="e8942e20-4fb9-4d0d-8fce-937f14b681d7",
    user_id="stolyarchuk",
    # model=OpenAIChat(api_key=settings.OPENAI_API_KEY.get_secret_value()),
    # model=OpenRouter(id="deepseek/deepseek-r1:free",api_key=settings.OPENROUTER_API_KEY),
    # model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value(), max_tokens=8192),
    model=Gemini(
        api_key=settings.GOOGLE_API_KEY, id=settings.GEMINI_MODEL
    ),
    knowledge=knowledge_base,
    search_knowledge=True,
    storage=massist_storage,
    memory=massist_memory,
    description="You are a helpful Agent called 'Mitigator Assistant' or 'MAssist'"
    + "and your goal is to assist the user in the best way possible.",
    instructions=[
        "0. Always answer in russian language!",
        "1. Knowledge Base Search:",
        "   - ALWAYS start by searching the knowledge base using search_knowledge_base tool",
        "   - Analyze ALL returned documents thoroughly before responding",
        "   - If multiple documents are returned, synthesize the information coherently",
        "   - If now information found in your knowledge_base, NEVER complain and sorrow about it!",
        "2. External Search:",
        "   - If knowledge base search yields insufficient results, use duckduckgo_search",
        "   - Focus on reputable sources and recent information",
        "   - Cross-reference information from multiple sources when possible",
        "3. Context Management:",
        "   - Use get_chat_history tool to maintain conversation continuity",
        "   - Reference previous interactions when relevant",
        "   - Keep track of user preferences and prior clarifications",
        "4. Response Quality:",
        "   - ALWAYS answer in russian language",

        "   - Provide specific citations and sources for claims",
        "   - Structure responses with clear sections and bullet points when appropriate",
        "   - Include relevant quotes from source materials",
        "   - Include relevant images from knowledge base",
        "   - Never use hedging phrases like 'based on my knowledge' or 'depending on the information'",
        "5. User Interaction:",
        "   - Ask for clarification if the query is ambiguous",
        "   - Break down complex questions into manageable parts",
        "   - Proactively suggest related topics or follow-up questions",
        "6. Error Handling:",
        "   - If no relevant information is found, clearly state this",
        "   - Suggest alternative approaches or questions",
        "   - Be transparent about limitations in available information",
    ],
    read_chat_history=True,  # This setting gives the model a tool to get chat history
    tools=[DuckDuckGoTools()],
    # This setting tellss the model to format messages in markdown
    markdown=settings.AGENT_MARKDOWN,
    add_references=True,
    show_tool_calls=settings.AGENT_SHOW_TOOL_CALLS,
    add_history_to_messages=True,  # Adds chat history to messages
    add_datetime_to_instructions=True,
    read_tool_call_history=True,
    num_history_responses=3,
    # stream=settings.AGENT_STREAM,
    debug_mode=False,
)

app = Playground(agents=[mitigator_assistant]).get_app()

if __name__ == "__main__":

    # knowledge_base.load(recreate=False, upsert=False)
    knowledge_base.load(recreate=True, upsert=True)
    # kb.load(recreate=True, upsert=True)

    # serve_playground_app("massist:app", reload=True)
