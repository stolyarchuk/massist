from llmx.knowledge import get_kb
from llmx.logger import init_logging
from llmx.models import vllm_model

init_logging()

if __name__ == "__main__":
    get_kb("integrate", vllm_model).load(recreate=True, upsert=True)
