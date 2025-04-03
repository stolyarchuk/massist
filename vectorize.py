import anyio

from massist.knowledge import get_kb
from massist.logger import init_logging
from massist.models import (get_deepseek_model, get_gemini_pri_model,
                            get_mistral_model, get_openrouter_model)


async def main():
    await init_logging()

    # chunking_model = get_mistral_model()
    chunking_model = get_deepseek_model(temperature=0.5)

    # get_kb(topic="index", chunking_model=chunking_model, max_links=20, max_depth=1).load(
    #     recreate=True, upsert=True
    # )


    

    # get_kb(topic="install", chunking_model=chunking_model,).load(
    #     recreate=True, upsert=True
    # )

    # get_kb(topic="integrate", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True
    # )

    # get_kb(topic="versions", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True
    # )
    # get_kb(topic="maintenance", chunking_model=get_deepseek_model(temperature=0.7)).load(
    #     recreate=True, upsert=True)
    # get_kb(topic="kb", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True)
    # get_kb(topic="psg", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True)
    # get_kb(topic="contact", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True)
    get_kb(topic="price", chunking_model=chunking_model).load(
        recreate=True, upsert=True)
    # get_kb(topic="collector").load(recreate=True, upsert=True)
    # pass


if __name__ == "__main__":
    anyio.run(main)
