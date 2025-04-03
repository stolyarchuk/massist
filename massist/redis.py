from contextlib import AbstractAsyncContextManager
from typing import (Any, AsyncGenerator, AsyncIterator, ClassVar, Optional,
                    Sequence, Type)

import redis.asyncio as redisio
import ujson as json
from agno.agent.agent import Agent
from agno.team.team import Team
from pydantic import BaseModel, Field, model_validator
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool as RedisConnectionPool
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.exceptions import RedisError

from config import config
from massist.json_serializers import custom_serialize
from massist.logger import get_logger

CHAT_IDX_NAME = 'idx:session'
CHAT_IDX_PREFIX = 'session:'

logger = get_logger(__name__)


class AsyncRedisPoolContext(AbstractAsyncContextManager):
    pool: RedisConnectionPool
    connection: Redis | None = None

    def __init__(self, max_connection: int = 100):
        self.pool = RedisConnectionPool.from_url(
            url=config.REDIS_URL,
            encoding="utf-8",
            decode_responses=False
        )

    async def get_connection(self) -> Redis:
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
        self.connection = await self.get_connection()
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

    async def close(self):
        """Close the connection pool and release all connections."""
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
    return redisio.from_url(
        config.REDIS_URL,
        encoding="utf-8",
        decode_responses=False
    )


async def create_chat_index(rdb: Redis):
    logger.debug(f"Creating Redis index '{CHAT_IDX_NAME}'")

    try:
        schema: Sequence[TextField] = [
            TextField('$.session_id', as_name='session_id', sortable=True,)
        ]

        await rdb.ft(CHAT_IDX_NAME).create_index(
            fields=schema,
            definition=IndexDefinition(
                prefix=[CHAT_IDX_PREFIX],
                index_type=IndexType.JSON
            )
        )
        logger.info(f"Redis index '{CHAT_IDX_NAME}' created successfully")
    except Exception as e:
        logger.warning(f"Error creating chat index '{CHAT_IDX_NAME}': {e}")


async def setup_redis_pool(rdb: Redis):
    logger.debug('Setting up Redis DB')
    try:
        logger.debug(f"Getting Redis index '{CHAT_IDX_NAME}'")
        index_info = await rdb.ft(CHAT_IDX_NAME).info()
        logger.debug(f"Fetched Redis index '{CHAT_IDX_NAME}' '{index_info}'")
    except Exception:
        await create_chat_index(rdb)


class RedisCache:
    def __init__(self, redis_pool: Redis, prefix: str = "cache"):
        self.redis = redis_pool
        self.prefix = prefix

    def _key(self, key: str) -> str:
        return f"{self.prefix}:{key}"

    async def set_model(
        self,
        key: str,
        model: Any,
        ex: Optional[int] = None
    ) -> bool:
        """Cache a Pydantic model with expiration"""
        try:
            logger.debug(f"Caching '{model}'. Key: {key}.")

            # Handle different types of models
            if isinstance(model, (Agent, Team)):
                # Use custom serialization for Agent and Team objects
                serialized = custom_serialize(model)
            elif isinstance(model, BaseModel):
                # Standard Pydantic model
                serialized = json.dumps(model.model_dump())
            elif isinstance(model, dict):
                # Dictionary
                serialized = json.dumps(model)
            elif isinstance(model, str):
                # Already serialized string
                serialized = model
            else:
                # Fallback
                serialized = custom_serialize(model)

            result = await self.redis.set(
                name=self._key(key),
                value=serialized,
                ex=ex or config.CACHE_TTL
            )

            logger.debug(f"Cached '{model}. Result: {result}.")
            return True
        except (TypeError, ValueError, RedisError) as e:
            logger.error(f"Caching failed: {str(e)}")
            return False

    async def get_model(
        self,
        key: str,
        model_type: Type[BaseModel]
    ) -> Optional[BaseModel]:
        """Retrieve and deserialize a cached model"""

        logger.debug("Trying to get model '%s' from cache.", key)

        try:
            data = await self.redis.get(self._key(key))

            if data:
                return model_type(**json.loads(data))

        except (json.JSONDecodeError, RedisError) as e:
            logger.error(f"Cache get failed: {str(e)}")
            await self.delete(key)  # Clean invalid entries
        return None

    async def delete(self, key: str) -> int:
        """Remove cached entry"""
        return await self.redis.delete(self._key(key))


async def init_redis():
    logger.debug("Initializing KV: %s", config.REDIS_URL)

    async with AsyncRedisPoolContext() as rdb:
        await setup_redis_pool(rdb)

    logger.debug('KV initialized %s', config.REDIS_URL)


# async def cache_model(
#     key: str,
#     model: BaseModel,
#     rdb: Redis = get_redis_pool(),
#     prefix: str = "lead"
# ):
#     cache = RedisCache(redis_pool=rdb)

#     return await cache.set_model(f"{prefix}:{key}", model, ex=7200)
