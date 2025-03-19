# Standard library imports
import logging
from typing import List

# Agno imports
from agno.agent.agent import Agent
from agno.document.chunking.agentic import AgenticChunking
from agno.document.chunking.semantic import SemanticChunking
from agno.document.reader.firecrawl_reader import FirecrawlReader
from agno.embedder.cohere import CohereEmbedder
from agno.embedder.google import GeminiEmbedder
from agno.embedder.ollama import OllamaEmbedder
from agno.knowledge.document import DocumentKnowledgeBase
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.memory.agent import AgentMemory
from agno.memory.classifier import MemoryClassifier
from agno.memory.db.postgres import PgMemoryDb
from agno.memory.manager import MemoryManager
from agno.models.deepseek.deepseek import DeepSeek
from agno.models.google.gemini import Gemini
from agno.models.ollama.chat import Ollama
from agno.models.ollama.tools import OllamaTools
from agno.models.openai.chat import OpenAIChat
from agno.models.openrouter.openrouter import OpenRouter
# from agno.models.openai.like import OpenAILike
from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app
from agno.reranker.base import Reranker
from agno.reranker.cohere import CohereReranker
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

from config import config
# Local imports
from logger import init_module_loggers, update_formatters


class MAssist(Workflow):
    pass


load_dotenv()
# loggers = [logging.getLogger().name]
# loggers += list(logging.Logger.manager.loggerDict.keys())

loggers = list(logging.Logger.manager.loggerDict.keys())

# update_formatters(*loggers)
init_module_loggers(*loggers)

# Initialize Ollama client
ollama_embedder = OllamaClient(host=config.OLLAMA_HOST)
ollama_chunker = OllamaClient(host=config.OLLAMA_HOST)


class DecoratedOllamaEmbedder(OllamaEmbedder):
    def get_embedding(self, text: str) -> List[float]:
        try:
            response = self._response(text=text)

            if response is None or "embeddings" not in response or not response.get("embeddings", []):
                return []

            response_embeddings = response.get("embeddings", [])
            if len(response_embeddings) > 1:
                raise ValueError(
                    "Expected a single embedding, but received multiple embeddings")

            return response_embeddings[0]
        except Exception as e:
            logger.warning(e)
            return []


# class DecoratedReranker(Reranker):
#     def rerank(self, query: str, documents: List[Document]) -> List[Document]:

#     def get_embedding(self, text: str) -> List[float]:
#         try:
#             response = self._response(text=text)

#             if response is None or "embeddings" not in response or not response.get("embeddings", []):
#                 return []

#             response_embeddings = response.get("embeddings", [])
#             if len(response_embeddings) > 1:
#                 raise ValueError("Expected a single embedding, but received multiple embeddings")

#             return response_embeddings[0]
#         except Exception as e:
#             logger.warning(e)
#             return []

# freader = FirecrawlReader(
#     api_key=settings.FIRECRAWL_API_KEY,
#     mode="scrape",
#     chunk=True,
#     # for crawling
#     # params={
#     #     'limit': 5,
#     #     'scrapeOptions': {'formats': ['markdown']}
#     # }
#     # for scraping
#     params={"formats": ["markdown"]},
# )


# dos = reader.read(settings.WEBSITE_URL)
# kb = DocumentKnowledgeBase(
#     documents=freader.read(settings.WEBSITE_URL),
#     vector_db=PgVector(
#         db_url=settings.DB_URL,
#         table_name="massist_embeddings",
#         schema="ai",
#         embedder=CohereEmbedder(
#             api_key=settings.COHERE_API_KEY, dimensions=settings.COHERE_DIMENSIONS, id=settings.COHERE_MODEL
#         ),
#         reranker=CohereReranker(api_key=settings.COHERE_API_KEY, model="rerank-multilingual-v3.0"),
#         search_type=SearchType.hybrid,
#     ),
#     num_documents=3,
#     chunking_strategy=AgenticChunking(
#         model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value()), max_chunk_size=1000
#     ),
# )


knowledge_base = WebsiteKnowledgeBase(
    # reader=freader,
    urls=[config.WEBSITE_URL],
    # Number of links to follow from the seed URLs
    max_links=80,
    max_depth=6,
    vector_db=PgVector(
        db_url=config.DB_URL,
        table_name="massist_embeddings",
        schema="ai",
        embedder=GeminiEmbedder(
            api_key=config.GOOGLE_API_KEY.get_secret_value()),
        # embedder=CohereEmbedder(
        #     api_key=settings.COHERE_API_KEY, dimensions=settings.COHERE_DIMENSIONS, id=settings.COHERE_MODEL
        # ),
        # reranker=CohereReranker(api_key=settings.COHERE_API_KEY, model="rerank-multilingual-v3.0"),
        # embedder=OllamaEmbedder(
        #     # id="deepseek-r1:7b",
        #     id="paraphrase-multilingual",
        #     # id="twine/noinstruct-small-embedding-v0",
        #     # ollama_client=ollama_embedder,
        #     dimensions=768,
        #     host=settings.OLLAMA_HOST,
        # ),
        # reranker=DecoratedOllamaEmbedder(
        #     # id="deepseek-r1:7b",
        #     id="bge-m3",
        #     ollama_client=ollama_client,
        #     dimensions=768,
        #     host=settings.OLLAMA_HOST,
        # ),
        search_type=SearchType.hybrid,
    ),
    num_documents=5,
    chunking_strategy=AgenticChunking(
        model=Gemini(api_key=config.GOOGLE_API_KEY), max_chunk_size=5000
    ),
    # chunking_strategy=AgenticChunking(
    #     model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value(), max_tokens=8192), max_chunk_size=1000
    # ),
    # chunking_strategy=SemanticChunking(
    #     embedder=GeminiEmbedder(api_key=settings.GOOGLE_API_KEY.get_secret_value(), id="text-embedding-3-small"),
    # ),
    # chunking_strategy=AgenticChunking(
    #     model=OllamaTools(id="deepseek-r1:14b", host=settings.OLLAMA_HOST), max_chunk_size=1000
    # ),
    # chunking_strategy=AgenticChunking(
    # model=OpenAIChat(api_key=settings.OPENAI_API_KEY.get_secret_value()), max_chunk_size=1000
    # ),
    # chunking_strategy=AgenticChunking(
    # model=OpenRouter(id="deepseek/deepseek-r1:free",api_key=settings.OPENROUTER_API_KEY), max_chunk_size=1000
    # ),
)

massist_memory = AgentMemory(
    # Persist memory in Postgres
    db=PgMemoryDb(table_name="massist_memory", db_url=config.DB_URL),
    create_user_memories=True,  # Store user preferences
    create_session_summary=True,  # Store conversation summaries
    # classifier=MemoryClassifier(
    #     # Classify memory based on user preferences
    #     # model=OllamaTools(id="deepseek-r1:14b", host=settings.OLLAMA_HOST),
    #     model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value()),
    # ),
    # manager=MemoryManager(
    #     # Manage memory with a focus on user preferences
    #     # model=OllamaTools(id="deepseek-r1:14b", host=settings.OLLAMA_HOST),
    #     model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value()),
    # ),
)

mmanager_memory = AgentMemory(
    # Persist memory in Postgres
    db=PgMemoryDb(table_name="mmanager_memory", db_url=config.DB_URL),
    create_user_memories=True,  # Store user preferences
    create_session_summary=True,  # Store conversation summaries
    # classifier=MemoryClassifier(
    #     # Classify memory based on user preferences
    #     # model=OllamaTools(id="deepseek-r1:14b", host=settings.OLLAMA_HOST),
    #     model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value()),
    # ),
    # manager=MemoryManager(
    #     # Manage memory with a focus on user preferences
    #     # model=OllamaTools(id="deepseek-r1:14b", host=settings.OLLAMA_HOST),
    #     model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value()),
    # ),
)

mitigator_assistant = Agent(
    name="Mitigator Assistant",
    agent_id="mitigator_assistant",
    # session_id=session_id,  # Track session ID for persistent conversations
    user_id="stolyarchuk",
    # model=OpenAIChat(api_key=settings.OPENAI_API_KEY.get_secret_value()),
    # model=OpenRouter(id="deepseek/deepseek-r1:free",api_key=settings.OPENROUTER_API_KEY),
    # model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value(), max_tokens=8192),
    model=Gemini(api_key=config.GOOGLE_API_KEY),
    # model=OllamaTools(id="gemma3:12b", host=settings.OLLAMA_HOST),
    knowledge=knowledge_base,
    search_knowledge=True,
    storage=PostgresStorage(table_name="massist_sessions",
                            db_url=config.DB_URL),  # Persist session data
    memory=massist_memory,  # Add memory to the agent
    description="You are a helpful Agent called 'Mitigator Assistant' or 'MAssist'"
    + "and your goal is to assist the user in the best way possible.",
    instructions=[
        "0. Always answer in russian language!",
        "1. Knowledge Base Search:",
        "   - ALWAYS start by searching the knowledge base using search_knowledge_base tool",
        "   - Analyze ALL returned documents thoroughly before responding",
        "   - If multiple documents are returned, synthesize the information coherently",
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
        "   - Avoid hedging phrases like 'based on my knowledge' or 'depending on the information'",
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
    markdown=config.AGENT_MARKDOWN,
    # add_chat_history_to_messages=True,
    add_references=True,
    show_tool_calls=False,
    add_history_to_messages=True,  # Adds chat history to messages
    add_datetime_to_instructions=True,
    read_tool_call_history=True,
    num_history_responses=3,
    stream=config.AGENT_STREAM,
    debug_mode=False,
)


mitigator_manager = Agent(
    name="Mitigator Manager",
    agent_id="mitigator_manager",
    team=[mitigator_assistant],
    description="You are a person who is talking to the outside world. You are listening your team and answer.",
    instructions=[
        # "Always use russian language in your answers",
        "First, ask mitigator_assistant for what the user is asking about.",
        "Always answer from mitigator_assistant person",
        "Finally, provide a thoughtful and engaging summary from mitigator_assistant.",
    ],
    # reasoning=True,
    memory=mmanager_memory,
    model=Gemini(api_key=config.GOOGLE_API_KEY.get_secret_value()),
    # model=OpenAIChat(api_key=settings.OPENAI_API_KEY.get_secret_value()),
    # model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value(), max_tokens=8192),
    # model=OllamaTools(id="deepseek-r1:14b", host=settings.OLLAMA_HOST),
    show_tool_calls=False,
    storage=PostgresStorage(table_name="mitigator_manager_sessions",
                            db_url=config.DB_URL),  # Persist session data
    add_history_to_messages=True,  # Adds chat history to messages
    add_datetime_to_instructions=True,
    # read_tool_call_history=True,
    markdown=config.AGENT_MARKDOWN,
    stream=config.AGENT_STREAM,
    # reasoning_max_steps=2
    # debug_mode=True,
)

app = Playground(
    agents=[mitigator_assistant],
).get_app()

if __name__ == "__main__":

    # knowledge_base.load(recreate=False, upsert=False)
    knowledge_base.load(recreate=True, upsert=True)
    # kb.load(recreate=True, upsert=True)

    # serve_playground_app("massist:app", reload=True)
