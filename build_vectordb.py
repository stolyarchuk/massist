from llmx.knowledge import get_kb
from llmx.logger import init_logging

init_logging()

if __name__ == "__main__":

    # Load the knowledge base and recreate the vector database
    get_kb(1001).load(recreate=True, upsert=True)
