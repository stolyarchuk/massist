import asyncio
from typing import Any, AsyncIterator, Dict, Optional

import ujson
from agno.run.team import TeamRunResponse
from agno.team.team import Team
from pydantic import BaseModel, ConfigDict, Field

from massist.json_serializers import custom_serialize
from massist.logger import get_logger
from massist.models import get_gemini_pri_model, get_gemini_sec_model
from massist.redis import Redis, RedisCache, get_redis_pool
from massist.storage_db import get_storage
from massist.team import get_mitigator_team

logger = get_logger(__name__)


class TeamLead(BaseModel):
    user_id: str
    session_id: str
    storage_id: str = "guest"
    memory_id: str = "guest"
    mitigator_team: Optional[Team] = Field(default=None, exclude=True)

    def model_post_init(self, context: Any, /) -> None:
        """Initialize the mitigator team after all attributes are set."""
        logger.debug("Post initializing BaseModel. context: %s", context)

        if self.mitigator_team:
            logger.warning("Replacing team. TeamLead session_id: %s",
                           context.session_id)

        # The context is passed automatically by Pydantic
        # We use self.user_id and self.session_id since they would have been set by Pydantic
        self.mitigator_team = get_mitigator_team(
            user_id=self.user_id,
            session_id=self.session_id,
            model=get_gemini_pri_model()
        )

    async def arun_stream(self, message: str) -> AsyncIterator[str]:
        error_data = {
            "error": "Invalid input: message must be a non-empty string"}

        if not message or not isinstance(message, str):
            yield ujson.dumps({"event": "error", "data": error_data})
            return

        yield ujson.dumps({"event": "start", "data": ""})

        try:
            response_stream:  AsyncIterator[TeamRunResponse] = await self.mitigator_team.arun(  # type: ignore
                message=message, stream_intermediate_steps=True, stream=True
            )

            async for chunk in response_stream:  # type: ignore
                if not chunk:  # Skip empty chunks
                    continue

                if isinstance(chunk, TeamRunResponse):
                    yield ujson.dumps({"event": "message", "data": chunk.to_dict()})
                elif isinstance(chunk, dict):
                    yield ujson.dumps({"event": "message", "data": chunk})
                else:
                    yield ujson.dumps({"event": "message", "data": str(chunk)})

        except asyncio.CancelledError as e:
            logger.warning("team_lead: %s", e)
            yield ujson.dumps({"event": "cancelled", "data": {"content": "Stream cancelled"}})
            return

        except Exception as e:
            logger.error("team_lead_b: %s", e)
            error_details = {
                "error": str(e),
                "type": type(e).__name__
            }
            yield ujson.dumps({"event": "error", "data": error_details})

        finally:
            yield ujson.dumps({"event": "end", "data": ""})

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        # Exclude Team from JSON serialization
        json_encoders={Team: lambda v: None}
    )


async def cache_team_lead(
    teamlead: TeamLead,
    rdb: Redis = get_redis_pool(),
    prefix: str = "teamlead"
) -> bool:
    cache = RedisCache(redis_pool=rdb)

    return await cache.set_model(f"{prefix}:{teamlead.session_id}", teamlead, ex=7200)


async def get_cached_teamlead(
    session_id: str,
    rdb: Redis = get_redis_pool(),
    prefix: str = "teamlead"
) -> Optional[TeamLead]:
    """
    Retrieves a TeamLead profile from cache if it exists.

    Args:
        session_id: The unique session identifier
        rdb: Redis connection pool
        prefix: Cache key prefix

    Returns:
        The TeamLead object if found in cache, None otherwise
    """
    cache = RedisCache(redis_pool=rdb)
    cached_data = await cache.get_model(f"{prefix}:{session_id}", TeamLead)

    logger.warning("get_model %s", cached_data)

    if not cached_data:
        return None

    # When creating a new TeamLead instance, you can pass context data
    # The context will automatically be passed to model_post_init
    context = {"session_id": session_id}

    # Use model_validate with context
    return TeamLead.model_validate(obj=cached_data, context=context)


async def cache_teamlead(
    teamlead: TeamLead,
    rdb: Redis = get_redis_pool(),
    prefix: str = "teamlead"
):
    """Cache the TeamLead object in Redis."""
    cache = RedisCache(redis_pool=rdb, prefix=prefix)

    # Convert to dict and serialize with custom encoder
    data = teamlead.model_dump()
    try:
        serialized = custom_serialize(data)
        return await cache.set_model(f"{prefix}:{teamlead.session_id}", serialized, ex=7200)
    except Exception as e:
        logger.error(f"Caching failed: {e}")

        # Fall back to caching only essential data
        essential_data = {
            "user_id": teamlead.user_id,
            "session_id": teamlead.session_id,
            "storage_id": teamlead.storage_id,
            "memory_id": teamlead.memory_id
        }
        return await cache.set_model(f"teamlead:{teamlead.session_id}", ujson.dumps(essential_data), ex=7200)
