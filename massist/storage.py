from agno.storage.base import Storage
from agno.storage.mongodb import MongoDbStorage
from agno.storage.postgres import PostgresStorage
from agno.storage.sqlite import SqliteStorage

from massist.config import config


def get_storage(agent_id: str) -> Storage:
    if config.STORAGE_DB == "pg":
        return PostgresStorage(
            table_name=f"sessions_{agent_id}", db_url=config.POSTGRES_URL
        )

    if config.STORAGE_DB == "sqlite":
        return SqliteStorage(
            table_name=f"sessions_{agent_id}",
            db_file="tmp/data.db",
        )

    if config.STORAGE_DB == "mongo":
        return MongoDbStorage(
            collection_name=f"sessions_{agent_id}",
            db_url=config.MONGO_URL,
            db_name="ai",
        )

    raise ValueError("bad storage class name")
