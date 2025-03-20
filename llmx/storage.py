from agno.storage.mongodb import MongoDbStorage
from agno.storage.postgres import PostgresStorage

from config import config

pg_storage = PostgresStorage(
    table_name="massist_sessions",
    db_url=config.DB_URL
)

mongo_storage = MongoDbStorage(
    collection_name="massist_sessions",
    db_url=config.MONGO_URL,
    db_name="ai",
)
