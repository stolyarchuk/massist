from typing import List

from agno.agent.agent import Agent
from agno.document.chunking.agentic import AgenticChunking

# from agno.document.chunking.document import DocumentChunking
from agno.embedder.cohere import CohereEmbedder
from agno.embedder.ollama import OllamaEmbedder
from agno.knowledge.website import WebsiteKnowledgeBase
from agno.memory.agent import AgentMemory
from agno.memory.classifier import MemoryClassifier
from agno.memory.db.postgres import PgMemoryDb
from agno.memory.manager import MemoryManager
from agno.models.deepseek.deepseek import DeepSeek
from agno.models.ollama.chat import Ollama
from agno.models.ollama.tools import OllamaTools
from agno.models.openai.chat import OpenAIChat
from agno.models.openai.like import OpenAILike
from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app
from agno.reranker.cohere import CohereReranker
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.utils.log import logger
from agno.vectordb.lancedb.lance_db import LanceDb
from agno.vectordb.pgvector.pgvector import PgVector
from agno.vectordb.search import SearchType
from dotenv import load_dotenv
from ollama import Client as OllamaClient

from logger import init_module_loggers, logging, update_formatters
from settings import settings

load_dotenv()
# loggers = [logging.getLogger().name]
# loggers += list(logging.Logger.manager.loggerDict.keys())

loggers = list(logging.Logger.manager.loggerDict.keys())

update_formatters(*loggers)
# init_module_loggers(*loggers)

# Initialize Ollama client
ollama_client = OllamaClient(host=settings.OLLAMA_HOST)


class DecoratedOllamaEmbedder(OllamaEmbedder):
    def get_embedding(self, text: str) -> List[float]:
        try:
            response = self._response(text=text)

            if response is None or "embeddings" not in response or not response.get("embeddings", []):
                return []

            response_embeddings = response.get("embeddings", [])
            if len(response_embeddings) > 1:
                raise ValueError("Expected a single embedding, but received multiple embeddings")

            return response_embeddings[0]
        except Exception as e:
            logger.warning(e)
            return []


knowledge_base = WebsiteKnowledgeBase(
    urls=[settings.WEBSITE_URL],
    # Number of links to follow from the seed URLs
    max_links=1000,
    max_depth=2,
    # Table name: ai.website_documents
    # vector_db=PgVector(
    #     table_name="mdocs_embeddings",
    #     db_url=settings.DB_URL,
    #     search_type=SearchType.hybrid,
    #     embedder=OllamaEmbedder(id="deepseek-r1:14b", dimensions=4096, host=settings.OLLAMA_HOST),
    # ),
    # vector_db=LanceDb(
    #     uri="tmp/lancedb",
    #     table_name="massist_kb",
    #     search_type=SearchType.vector,
    #     # embedder=DecoratedOllamaEmbedder(
    #     #     id="paraphrase-multilingual:latest", dimensions=768, ollama_client=ollama_client
    #     # ),
    #     embedder=CohereEmbedder(
    #         api_key=settings.COHERE_API_KEY, dimensions=settings.COHERE_DIMENSIONS, id=settings.COHERE_MODEL
    #     ),
    #     reranker=CohereReranker(api_key=settings.COHERE_API_KEY, model="rerank-multilingual-v3.0"),
    # ),
    vector_db=PgVector(
        db_url=settings.DB_URL,
        table_name="massist_embeddings",
        schema="ai",
        embedder=CohereEmbedder(
            api_key=settings.COHERE_API_KEY, dimensions=settings.COHERE_DIMENSIONS, id=settings.COHERE_MODEL
        ),
        reranker=CohereReranker(api_key=settings.COHERE_API_KEY, model="rerank-multilingual-v3.0"),
        search_type=SearchType.hybrid,
    ),
    #     embedder=DecoratedOllamaEmbedder(
    #         # id="deepseek-r1:7b",
    #         id="paraphrase-multilingual",
    #         ollama_client=ollama_client,
    #         dimensions=768,
    #         host=settings.OLLAMA_HOST,
    #     ),
    #     search_type=SearchType.hybrid,
    # ),
    num_documents=3,
    chunking_strategy=AgenticChunking(
        model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value()), max_chunk_size=1000
    ),
    # chunking_strategy=AgenticChunking(
    #     model=OllamaTools(id="deepseek-r1:14b", host=settings.OLLAMA_HOST), max_chunk_size=1000
    # ),
    # chunking_strategy=AgenticChunking(
    #     model=OpenAIChat(api_key=settings.OPENAI_API_KEY.get_secret_value()), max_chunk_size=1000
    # ),
)

massist_memory = AgentMemory(
    db=PgMemoryDb(table_name="massist_memory", db_url=settings.DB_URL),  # Persist memory in Postgres
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
    db=PgMemoryDb(table_name="mmanager_memory", db_url=settings.DB_URL),  # Persist memory in Postgres
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
    # model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value()),
    # model=OllamaTools(id="deepseek-r1:14b", host=settings.OLLAMA_HOST),
    knowledge=knowledge_base,
    storage=PostgresAgentStorage(table_name="massist_sessions", db_url=settings.DB_URL),  # Persist session data
    memory=massist_memory,  # Add memory to the agent
    description="You are a helpful Agent called 'Mitigator Assistant' or 'MAgent'"
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
    search_knowledge=True,
    read_chat_history=True,  # This setting gives the model a tool to get chat history
    tools=[DuckDuckGoTools()],
    markdown=True,  # This setting tellss the model to format messages in markdown
    # add_chat_history_to_messages=True,
    show_tool_calls=True,
    add_history_to_messages=True,  # Adds chat history to messages
    add_datetime_to_instructions=True,
    read_tool_call_history=True,
    num_history_responses=3,
    # stream=settings.AGENT_STREAM,
    debug_mode=True,
)

mitigator_translator = Agent(
    name="Mitigator Translator",
    agent_id="mitigator_translator",
    role="Translates from every language to russian",
    # model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value()),
    # model=OllamaTools(id="deepseek-r1:14b", host=settings.OLLAMA_HOST),
    # knowledge=knowledge_base,
    # search_knowledge=True,
    # read_tool_call_history=True,
    # read_chat_history=True,
    storage=PostgresAgentStorage(
        table_name="mitagator_translator_sessions", db_url=settings.DB_URL
    ),  # Persist session data
    description="You are a senior translator to russian. You lived for while in america and that's"
    + "why you know english very well. Given a message in not russian language,"
    + " your goal is to immidiately translate it to russian using all your knowledge of foreign languages.",
    instructions=[
        "Always translate what you hear.",
        "Always answer in Russian language.",
        "Important: Try not to use harmfull words.",
    ],
    # show_tool_calls=settings.AGENT_SHOW_TOOL_CALLS,
    markdown=settings.AGENT_MARKDOWN,
    # debug_mode=True,
    # stream=settings.AGENT_STREAM,
)

mitigator_manager = Agent(
    name="Mitigator Manager",
    agent_id="mitigator_manager",
    team=[mitigator_assistant, mitigator_translator],
    description="You are a person who is talking to the outside world. You are listening your team and answer.",
    instructions=[
        "Always use russian language in your answers",
        "First, ask mitigator_assistant for what the user is asking about.",
        "Then, ask mitigator_translator to translate into russian language.",
        "Finally, provide a thoughtful and engaging summary from mitigator_translator.",
    ],
    # reasoning=True,
    memory=mmanager_memory,
    # model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value()),
    # model=OllamaTools(id="deepseek-r1:14b", host=settings.OLLAMA_HOST),
    # show_tool_calls=True,
    storage=PostgresAgentStorage(
        table_name="mitagator_manager_sessions", db_url=settings.DB_URL
    ),  # Persist session data
    # add_history_to_messages=True,  # Adds chat history to messages
    # add_datetime_to_instructions=True,
    # read_tool_call_history=True,
    markdown=settings.AGENT_MARKDOWN,
    stream=settings.AGENT_STREAM,
    # debug_mode=True,
)

app = Playground(
    agents=[mitigator_manager],
).get_app()

if __name__ == "__main__":

    # knowledge_base.load(recreate=True, upsert=True)

    serve_playground_app("agno_scraper:app", reload=True)
