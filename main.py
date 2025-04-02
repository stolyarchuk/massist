import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import config
from massist.logger import init_logging, logger
from massist.redis import get_redis, get_redis_pool, setup_redis_pool
from massist.routes import router

init_logging()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router)


async def load_redis():
    async with get_redis_pool() as rdb:
        logger.debug('Setting up Redis DB')
        await setup_redis_pool(rdb)
        logger.debug('Redis DB initialized')


def main():
    logger.info("Entering main loop")
    asyncio.run(load_redis())


if __name__ == '__main__':
    main()
