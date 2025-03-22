from agno.storage.postgres import PostgresStorage
from agno.storage.sqlite import SqliteStorage

from config import config

pg_storage = PostgresStorage(
    table_name="massist_sessions",
    db_url=config.DB_URL
)

sqlite_storage = SqliteStorage(
    table_name="massist_sessions",
    db_file="tmp/data.db",
)
