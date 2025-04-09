from agno.memory.db.base import MemoryDb
from agno.memory.db.mongodb import MongoMemoryDb
from agno.memory.db.postgres import PgMemoryDb
from agno.memory.db.sqlite import SqliteMemoryDb

from config import config


def get_memory_db(agent_id: str) -> MemoryDb:
    if config.MEMORY_DB == "pg":
        return PgMemoryDb(table_name=f"memory_{agent_id}", db_url=config.POSTGRES_URL)

    if config.MEMORY_DB == "sqlite":
        return SqliteMemoryDb(
            table_name=f"memory_{agent_id}",
            db_file="tmp/data.db",
        )

    if config.MEMORY_DB == "mongo":
        return MongoMemoryDb(
            collection_name=f"memory_{agent_id}", db_url=config.MONGO_URL, db_name="ai"
        )

    raise ValueError("bad storage class name")
