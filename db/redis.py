from contextlib import AbstractAsyncContextManager
from dataclasses import asdict
from typing import Any, Optional, Sequence, Type

import redis.asyncio as redis
import ujson
from agno.agent.agent import Agent
from agno.team.team import Team
from pydantic import BaseModel
from redis.commands.json.path import Path
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.exceptions import RedisError

from config import config
from massist.logger import get_logger

logger = get_logger(__name__)


class RedisAsyncPool(AbstractAsyncContextManager):
    pool: redis.ConnectionPool | None = None
    connection: redis.Redis | None = None

    def __init__(self, max_connection: int = 100):
        self.pool = redis.ConnectionPool.from_url(
            url=config.REDIS_URL, encoding="utf-8", decode_responses=False
        )

    def get_connection(self) -> redis.Redis:
        """Get a Redis connection from the pool.

        Returns:
            Redis: A connection to the Redis server from the pool.
        """
        return redis.Redis(connection_pool=self.pool)

    async def __aenter__(self) -> redis.Redis:
        """Async enter context manager to get a Redis connection.

        Returns:
            Redis: An active Redis connection that can be used within the context.
        """
        self.connection = self.get_connection()
        return self.connection

    async def __aexit__(self, __exc_type, __exc_val, __exc_tb):
        """Close the Redis connection when exiting the context.

        Args:
            exc_type: The exception type if an exception was raised.
            exc_val: The exception value if an exception was raised.
            exc_tb: The traceback if an exception was raised.
        """
        if self.connection:
            await self.connection.aclose()
            self.connection = None

    def _key(self, key: str) -> str:
        return f"{key}"

    async def set_model(
        self, key: str, model: BaseModel | Any | str, ex: Optional[int] = None
    ) -> bool:
        """Cache a Pydantic model with expiration"""

        try:
            logger.debug(f"Caching '{model}'. Key: {key}.")

            if isinstance(model, (Agent, Team)):
                serialized = asdict(model)
            elif isinstance(model, BaseModel):
                serialized = ujson.loads(model.model_dump_json())
            elif isinstance(model, str):
                serialized = ujson.loads(model)
            elif hasattr(model, "__dict__"):  # Check if model has a __dict__ attribute
                serialized = model.__dict__
            else:
                serialized = asdict(model)

            async with self as redis:
                result = await redis.json().set(  # type: ignore
                    name=self._key(key),
                    path=Path.root_path(),
                    obj=serialized,
                    decode_keys=True,
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
            async with self as redis:
                data = await redis.json().get(self._key(key))  # type: ignore

                if data:
                    model = model_type(**data)
                    logger.debug("Model fetched from cache %s.", key)

        except (ujson.JSONDecodeError, RedisError) as e:
            logger.error(f"Cache get failed: {str(e)}")
            await self.delete(key)  # Clean invalid entries

        return model

    async def delete(self, key: str) -> int:
        """Remove cached entry"""
        async with self as rdb:
            deleted = await rdb.delete(self._key(key))
            logger.debug(f"Deleted cache entry '{key}'. Deleted: {deleted}.")

        return deleted

    async def aclose(self):
        """Close the Redis connection pool"""
        if self.pool:
            await self.pool.aclose()

    async def create_chat_index(self, rdb: redis.Redis):
        """Create the chat index in Redis if it doesn't exist."""
        logger.debug(f"Creating Redis index '{config.CHAT_IDX_NAME}'")

        try:
            schema: Sequence[TextField] = [
                TextField(
                    "$.teamlead.session_id",
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

    async def setup(self):
        """Set up Redis DB and create index if needed"""
        async with self as rdb:
            logger.debug("Setting up Redis DB")
            try:
                index_exists = await rdb.ft(config.CHAT_IDX_NAME).info()
                logger.debug(
                    f"Redis index '{config.CHAT_IDX_NAME}' exists: '{index_exists}'"
                )
            except Exception:
                await self.create_chat_index(rdb)


async def init_redis():
    """Initialize Redis connection and set up the database"""
    logger.debug("Initializing KV: %s", config.REDIS_URL)

    rcp = RedisAsyncPool()
    await rcp.setup()

    logger.debug("KV initialized %s", config.REDIS_URL)
    return rcp
