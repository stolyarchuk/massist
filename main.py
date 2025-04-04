# import asyncio
import asyncio
from contextlib import asynccontextmanager

# import anyio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import config
from massist.logger import init_logging
from massist.redis import get_redis_pool, init_redis
from massist.router import router

ALLOW_ORIGINS = config.ALLOW_ORIGINS


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Redis on startup

    # async with anyio.create_task_group() as tg:
    #     tg.start_soon(init_logging)
    #     tg.start_soon(init_redis)

    # await init_logging('uvicorn.access', 'uvicorn.error', 'httpx', 'asyncio', 'uvicorn', 'agno', 'agno-team')
    await init_logging()
    await init_redis()

    yield

    # Close Redis connections on shutdown
    redis_pool = get_redis_pool()
    await redis_pool.aclose()

    # TODO: close db connections as well

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router, prefix="/v1")
