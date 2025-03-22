from agno.storage.sqlite import SqliteStorage

from config import config


def get_storage(num: int):
    return SqliteStorage(
        table_name="massist_sessions",
        db_file=f"tmp/data_{num}.db",
    )
