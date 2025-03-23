from agno.storage.base import Storage
from agno.storage.postgres import PostgresStorage
from agno.storage.sqlite import SqliteStorage

from config import config


def get_storage(topic: str) -> Storage:
    if config.STORAGEDB_TYPE == "pg":
        return PostgresStorage(
            table_name=f"massist_sessions_{topic}",
            db_url=config.DB_URL
        )

    if config.STORAGEDB_TYPE == "sqlite":
        return SqliteStorage(
            table_name=f"massist_sessions_{topic}",
            db_file="tmp/data.db",
        )

    raise ValueError("bad storage class name")
