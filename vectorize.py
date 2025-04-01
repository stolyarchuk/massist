from massist.knowledge import get_kb
from massist.logger import init_logging
from massist.models import (get_deepseek_model, get_gemini_pri_model,
                            get_mistral_model, get_openrouter_model)

init_logging()

if __name__ == "__main__":
    chunking_model = get_mistral_model()

    # get_kb(topic="index", model=chunking_model, max_links=20, max_depth=1).load(
    #     recreate=True, upsert=True
    # )

    # get_kb(topic="install", model=chunking_model,).load(
    #     recreate=True, upsert=True
    # )

    # get_kb(topic="integrate", model=chunking_model).load(
    #     recreate=True, upsert=True
    # )
    # get_kb(topic="versions", model=chunking_model).load(
    #     recreate=True, upsert=True
    # )
    get_kb(topic="maintenance", model=get_deepseek_model(temperature=0.7), max_links=20).load(
        recreate=True, upsert=True)
    # get_kb(topic="kb").load(recreate=True, upsert=True)
    # get_kb(topic="psg").load(recreate=True, upsert=True)
    # get_kb(topic="contact").load(recreate=True, upsert=True)
    # get_kb(topic="price").load(recreate=True, upsert=True)
    # get_kb(topic="collector").load(recreate=True, upsert=True)
    # pass
