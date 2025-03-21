from llmx.knowledge import knowledge_base
from llmx.logger import init_logging

init_logging()

if __name__ == "__main__":
    # Load the knowledge base and recreate the vector database
    knowledge_base.load(recreate=True, upsert=True)
    print("Knowledge base loaded and vector database recreated.")
