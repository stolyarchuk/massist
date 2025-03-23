from config import config
from llmx.knowledge import get_kb
from llmx.logger import init_logging

init_logging()

if __name__ == "__main__":
    get_kb(config.VECTORDB_TYPE, config.DIMENSIONS).load(
        recreate=True, upsert=True)
