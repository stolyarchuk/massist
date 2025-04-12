# import asyncio
from contextlib import asynccontextmanager

# import anyio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bot import start_bot_nonblock
from config import config
from massist.logger import init_logging
from massist.redis import init_redis
from massist.router import router

ALLOW_ORIGINS = config.ALLOW_ORIGINS


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Redis on startup

    await init_logging()
    # await init_logging(
    #     "uvicorn.access",
    #     "aiogram.dispatcher",
    #     "uvicorn.error",
    #     "httpx",
    #     "asyncio",
    #     "uvicorn",
    #     "agno",
    #     "agno-team",
    # )

    app.state.redis = await init_redis()
    app.state.bot = await start_bot_nonblock()
    app.state.db = None  # TODO: Initialize your database connection here

    yield

    await app.state.bot.stop_polling()

    # Close Redis connections on shutdown
    async with app.state.redis as rdb:
        await rdb.aclose()  # noqa

    # TODO: close db connections as well


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/v1")
