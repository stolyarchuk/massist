import asyncio
from typing import Any, AsyncGenerator, AsyncIterator, Iterator, Optional

import ujson
from agno.run.team import TeamRunResponse
from agno.storage.base import Storage
from agno.team.team import Team
from pydantic import BaseModel, ConfigDict, Field

from massist.logger import logger
from massist.models import get_gemini_pri_model, get_gemini_sec_model
from massist.redis import RedisCache, get_redis_pool
from massist.storage_db import get_storage
from massist.team import get_mitigator_team


class TeamLead(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    user_id: str = ""
    session_id: str = ""
    storage_id: str = "lead"  # Store the ID instead of the object
    memory_id: str = "lead"  # Store the ID instead of the object

    mitigator_team: Team = get_mitigator_team(
        user_id=user_id,
        session_id=session_id,
        model=get_gemini_pri_model(),
        memory_model=get_gemini_sec_model()
    )

    @property
    def storage(self) -> Storage:
        return get_storage(self.storage_id)

    def __init__(self, user_id: str, session_id: str):
        super().__init__(user_id=user_id, session_id=session_id)
        self.mitigator_team = get_mitigator_team(
            user_id=self.user_id,
            session_id=self.session_id,
            model=get_gemini_pri_model(),
            memory_model=get_gemini_sec_model()
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


async def cache_user_profile(lead: TeamLead, prefix: str = "teamlead"):
    cache = RedisCache(redis_pool=get_redis_pool(), prefix=prefix)
    return await cache.set_model(f"lead:{lead.session_id}", lead, ex=7200)


async def get_cached_profile(session_id: str, prefix: str = "teamlead") -> Optional[BaseModel]:
    cache = RedisCache(redis_pool=get_redis_pool(), prefix=prefix)
    return await cache.get_model(f"lead:{session_id}", TeamLead)
