from agno.storage.base import Storage
from agno.storage.postgres import PostgresStorage
from agno.storage.sqlite import SqliteStorage

from config import config


def get_storage(name: str, num: int) -> Storage:
    """
    Return a storage backend based on provided name.

    Args:
        name (str): Storage type ('pg' for PostgreSQL or 'sqlite' for SQLite)
        num (int): Numerical identifier used for SQLite db filename

    Returns:
        Storage: Configured storage instance
    """
    if name == "pg":
        return PostgresStorage(
            table_name="massist_sessions",
            db_url=config.DB_URL
        )

    if name == "sqlite":
        return SqliteStorage(
            table_name="massist_sessions",
            db_file=f"tmp/data_{num}.db",
        )

    raise ValueError("bad storage class name")
