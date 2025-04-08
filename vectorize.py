import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from dotenv import load_dotenv

from config import config
from massist.knowledge import get_kb
from massist.logger import init_logging
from massist.models import get_mistral_model

load_dotenv()


def load_kb(
    topic: str, max_links: int = config.MAX_LINKS, max_depth: int = config.MAX_DEPTH
):
    """Load knowledge base for a specific topic."""
    get_kb(
        topic=topic,
        chunking_model=get_mistral_model(),
        max_links=max_links,
        max_depth=max_depth,
    ).load(recreate=True, upsert=True)


async def aload_kb(
    topic: str, max_links: int = config.MAX_LINKS, max_depth: int = config.MAX_DEPTH
):
    """Load knowledge base for a specific topic."""
    await get_kb(
        topic=topic,
        chunking_model=get_mistral_model(),
        max_links=max_links,
        max_depth=max_depth,
    ).aload(recreate=True, upsert=True)


async def main():
    await init_logging()

    chunking_model = get_mistral_model()
    # chunking_model = get_deepseek_model(temperature=0.5)

    # await asyncio.gather(
    #     get_kb(
    #         topic="index", chunking_model=chunking_model, max_links=20, max_depth=1
    #     ).aload(recreate=True, upsert=True),
    # get_kb(
    #     topic="install",
    #     chunking_model=chunking_model,
    # ).async_load(recreate=True, upsert=True),
    # get_kb(topic="integrate", chunking_model=chunking_model).aload(
    #     recreate=True, upsert=True
    # ),
    # get_kb(topic="versions", chunking_model=chunking_model).aload(
    #     recreate=True, upsert=True
    # ),
    # get_kb(topic="maintenance", chunking_model=get_deepseek_model(temperature=0.7)).aload(
    #     recreate=True, upsert=True
    # ),
    # get_kb(topic="kb", chunking_model=chunking_model).aload(
    #     recreate=True, upsert=True
    # ),
    # get_kb(topic="psg", chunking_model=chunking_model).aload(
    #     recreate=True, upsert=True
    # ),
    # get_kb(topic="contact", chunking_model=chunking_model).aload(
    #     recreate=True, upsert=True
    # ),
    # get_kb(topic="price", chunking_model=chunking_model).aload(
    #     recreate=True, upsert=True
    # ),
    # )

    get_kb(
        topic="index", chunking_model=chunking_model, max_links=20, max_depth=1
    ).load(recreate=True, upsert=True)

    # get_kb(topic="install", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True
    # )

    # get_kb(topic="integrate", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True
    # )

    # get_kb(topic="versions", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True
    # )
    # get_kb(topic="maintenance", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True)
    get_kb(topic="kb", chunking_model=chunking_model).load(recreate=True, upsert=True)
    # get_kb(topic="psg", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True)
    # get_kb(topic="contact", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True)
    # get_kb(topic="price", chunking_model=chunking_model).load(
    #     recreate=True, upsert=True
    # )
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as pool:
        # await loop.run_in_executor(
        #     pool, partial(load_kb, topic="install")
        # )

        # await loop.run_in_executor(
        #     pool, partial(load_kb, topic="integrate")
        # )

        # await loop.run_in_executor(
        #     pool, partial(load_kb, topic="versions")
        # )

        # await loop.run_in_executor(
        #     pool, partial(load_kb, topic="maintenance")
        # )

        # await loop.run_in_executor(
        #     pool, partial(load_kb, topic="psg")
        # )

        await loop.run_in_executor(
            pool, partial(load_kb, topic="index", max_links=20, max_depth=1)
        )

        await loop.run_in_executor(pool, partial(load_kb, topic="kb"))

    # load_kb(topic="index", max_links=20, max_depth=1)
    # load_kb(topic="kb")

    # get_kb(topic="collector").load(recreate=True, upsert=True)
    # pass


if __name__ == "__main__":
    asyncio.run(main())
