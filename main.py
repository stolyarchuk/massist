from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import config
from massist.logger import init_logging
from massist.redis import RedisCache, get_rdb, get_redis_pool, init_redis
from massist.routes import router

ALLOW_ORIGINS = ['*']

init_logging()


# Setup startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Redis on startup
    await init_redis()
    yield
    # Close Redis connections on shutdown
    redis_pool = get_redis_pool()
    await redis_pool.aclose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router)
