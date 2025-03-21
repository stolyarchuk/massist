from agno.storage.postgres import PostgresStorage

from config import config

pg_storage = PostgresStorage(
    table_name="massist_sessions",
    db_url=config.DB_URL
)
