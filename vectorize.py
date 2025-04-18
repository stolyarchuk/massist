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
    ).aload(recreate=False, upsert=True)


async def main():
    await init_logging()

    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as pool:
        await asyncio.gather(
            loop.run_in_executor(pool, partial(load_kb, topic="index", max_depth=1)),
            # loop.run_in_executor(pool, partial(load_kb, topic="install")),
            # loop.run_in_executor(pool, partial(load_kb, topic="integrate")),
            # loop.run_in_executor(pool, partial(load_kb, topic="kb")),
            # loop.run_in_executor(pool, partial(load_kb, topic="versions")),
            # loop.run_in_executor(pool, partial(load_kb, topic="psg")),
            # loop.run_in_executor(pool, partial(load_kb, topic="maintenance")),
            # loop.run_in_executor(pool, partial(load_kb, topic="contact")),
            # loop.run_in_executor(pool, partial(load_kb, topic="price")),
        )


if __name__ == "__main__":
    asyncio.run(main())
