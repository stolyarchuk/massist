from agno.memory.agent import AgentMemory
from agno.memory.classifier import MemoryClassifier
from agno.memory.db.mongodb import MongoMemoryDb
from agno.memory.db.postgres import PgMemoryDb
from agno.memory.manager import MemoryManager
from agno.memory.summarizer import MemorySummarizer

from config import config
from llmx.models import massist_memory_model

pg_memory = PgMemoryDb(
    table_name="massist_memory",
    db_url=config.DB_URL
)


mongo_memory = MongoMemoryDb(
    collection_name="massist_memory",
    db_url=config.MONGO_URL,
    db_name="ai"
)


massist_memory = AgentMemory(
    user_id="stolyarchuk",
    db=pg_memory,
    create_user_memories=True,
    create_session_summary=True,
    manager=MemoryManager(model=massist_memory_model),
    classifier=MemoryClassifier(model=massist_memory_model),
    summarizer=MemorySummarizer(model=massist_memory_model),
)
