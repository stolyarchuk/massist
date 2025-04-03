import asyncio
from dataclasses import field
from typing import Any, Optional, Sequence, Type

import redis.asyncio as redis
import ujson as json
from pydantic import BaseModel, Field
from redis.asyncio.client import Redis
from redis.commands.search.field import NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.exceptions import RedisError

from config import config
from massist.logger import logger

CHAT_IDX_NAME = 'idx:chat'
CHAT_IDX_PREFIX = 'chat:'


def get_redis_pool() -> Redis:
    return redis.from_url(
        config.REDIS_URL,
        encoding="utf-8",
        decode_responses=False
    )


async def get_rdb():
    rdb = get_redis_pool()
    try:
        yield rdb
    finally:
        await rdb.aclose()


async def create_chat_index(rdb: Redis):
    logger.debug(f"Creating Redis index '{CHAT_IDX_NAME}'")

    try:
        schema: Sequence[NumericField] = [
            NumericField('$.created', as_name='created', sortable=True,)
        ]

        await rdb.ft(CHAT_IDX_NAME).create_index(
            fields=list(schema),
            definition=IndexDefinition(
                prefix=[CHAT_IDX_PREFIX], index_type=IndexType.JSON)
        )
        logger.info(f"Redis index '{CHAT_IDX_NAME}' created successfully")
    except Exception as e:
        logger.warning(f"Error creating chat index '{CHAT_IDX_NAME}': {e}")


async def setup_redis_pool(rdb: Redis):
    logger.debug('Setting up Redis DB')
    try:
        logger.debug(f"Getting Redis index '{CHAT_IDX_NAME}")
        await get_redis_pool().ft(CHAT_IDX_NAME).info()
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
        model: BaseModel,
        ex: Optional[int] = None
    ) -> bool:
        """Cache a Pydantic model with expiration"""
        try:
            serialized = model.model_dump_json()
            return await self.redis.set(
                self._key(key),
                serialized,
                ex=ex or config.CACHE_TTL
            )
        except (TypeError, ValueError, RedisError) as e:
            logger.error(f"Cache set failed: {str(e)}")
            return False

    async def get_model(
        self,
        key: str,
        model_type: Type[BaseModel]
    ) -> Optional[BaseModel]:
        """Retrieve and deserialize a cached model"""
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
    async with get_redis_pool() as rdb:

        await setup_redis_pool(rdb)
        logger.debug('Redis DB initialized')
