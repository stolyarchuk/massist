from contextlib import AbstractAsyncContextManager
from typing import Optional, Sequence, Type

import ujson
from agno.agent.agent import Agent
from agno.team.team import Team
from pydantic import BaseModel
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.exceptions import RedisError

from config import config
from mai.logger import get_logger

logger = get_logger(__name__)


class AsyncRedisPoolContext(AbstractAsyncContextManager):
    pool: ConnectionPool | None = None
    connection: Redis

    def __init__(self, max_connection: int = 100):
        self.pool = ConnectionPool.from_url(
            url=config.REDIS_URL, encoding="utf-8", decode_responses=False
        )

        self.connection = self.get_connection()

    def get_connection(self) -> Redis:
        """Get a Redis connection from the pool.

        Returns:
            Redis: A connection to the Redis server from the pool.
        """

        return Redis(connection_pool=self.pool)

    async def __aenter__(self) -> Redis:
        """Async enter context manager to get a Redis connection.

        Returns:
            Redis: An active Redis connection that can be used within the context.
        """
        self.connection = self.get_connection()
        return self.connection

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close the Redis connection when exiting the context.

        Args:
            exc_type: The exception type if an exception was raised.
            exc_val: The exception value if an exception was raised.
            exc_tb: The traceback if an exception was raised.
        """
        if self.connection:
            await self.connection.aclose()
            self.connection = None

        if self.pool:
            await self.pool.disconnect()


async def get_rdb():
    async with AsyncRedisPoolContext() as arpc:
        yield arpc

    # rdb = get_redis_pool()
    # try:
    #     yield rdb
    # finally:
    #     await rdb.aclose()


def get_redis_pool() -> Redis:
    return Redis.from_url(config.REDIS_URL, encoding="utf-8", decode_responses=False)


async def create_chat_index(rdb: Redis):
    logger.debug(f"Creating Redis index '{config.CHAT_IDX_NAME}'")

    try:
        schema: Sequence[TextField] = [
            TextField(
                "$.session_id",
                as_name="session_id",
                sortable=True,
            )
        ]

        await rdb.ft(config.CHAT_IDX_NAME).create_index(
            fields=schema,
            definition=IndexDefinition(
                prefix=[config.CHAT_IDX_PREFIX], index_type=IndexType.JSON
            ),
        )
        logger.info(f"Redis index '{config.CHAT_IDX_NAME}' created successfully")
    except Exception as e:
        logger.warning(f"Error creating chat index '{config.CHAT_IDX_NAME}': {e}")


async def setup_redis_pool(rdb: Redis):
    logger.debug("Setting up Redis DB")
    try:
        logger.debug(f"Getting Redis index '{config.CHAT_IDX_NAME}'")
        index_exists = await rdb.ft(config.CHAT_IDX_NAME).info()
        logger.debug(f"Redis index '{config.CHAT_IDX_NAME}' exists: '{index_exists}'")
    except Exception:
        await create_chat_index(rdb)


class RedisCache:
    def __init__(self, redis_pool: Redis, prefix: str = "cache"):
        self.redis = redis_pool
        self.prefix = prefix

    def _key(self, key: str) -> str:
        return f"{self.prefix}:{key}"

    async def set_model(
        self, key: str, model: BaseModel | str, ex: Optional[int] = None
    ) -> bool:
        """Cache a Pydantic model with expiration"""

        try:
            logger.debug(f"Caching '{model}'. Key: {key}.")

            # # Handle different types of models
            if isinstance(model, (Agent, Team)):
                # Use custom serialization for Agent and Team objects
                serialized = ujson.dumps(model)
            elif isinstance(model, BaseModel):
                # Standard Pydantic model
                serialized = model.model_dump_json()
            # elif isinstance(model, dict):
            #     # Dictionary
            #     serialized = ujson.dumps(model)
            elif isinstance(model, str):
                # Already serialized string
                serialized = model
            else:
                # Fallback
                serialized = ujson.dumps(model.model_dump())

            result = await self.redis.set(
                name=self._key(key), value=serialized, ex=ex or config.CACHE_TTL
            )

            logger.debug(f"Cached '{model}. Result: {result}.")
        except (TypeError, ValueError, RedisError) as e:
            logger.error(f"Caching failed: {str(e)}")
            return False

        return True

    async def get_model(
        self, key: str, model_type: Type[BaseModel]
    ) -> Optional[BaseModel]:
        """Retrieve and deserialize a cached model"""

        logger.debug("Trying to get model from cache: %s.", key)
        model = None

        try:
            data = await self.redis.get(self._key(key))

            if data:
                model = model_type(**ujson.loads(data))
                logger.debug("Model fetched from cache %s.", key)

        except (ujson.JSONDecodeError, RedisError) as e:
            logger.error(f"Cache get failed: {str(e)}")
            await self.delete(key)  # Clean invalid entries

        return model

    async def delete(self, key: str) -> int:
        """Remove cached entry"""
        return await self.redis.delete(self._key(key))


async def init_redis():
    logger.debug("Initializing KV: %s", config.REDIS_URL)

    async with AsyncRedisPoolContext() as rdb:
        await setup_redis_pool(rdb)

    logger.debug("KV initialized %s", config.REDIS_URL)
