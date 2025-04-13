import asyncio
from typing import Any, AsyncIterator, Optional

import ujson
from agno.run.team import TeamRunResponse
from agno.team.team import Team
from pydantic import BaseModel, ConfigDict

from massist.logger import get_logger
from massist.models import get_gemini_pri_model
from massist.team import get_mitigator_team

logger = get_logger(__name__)


class TeamLead(BaseModel):
    user_id: str
    session_id: str
    storage_id: str = "guest"
    memory_id: str = "guest"
    team: Optional[Team] = None

    def model_post_init(self, __context: Any) -> None:
        """Initialize the mitigator team after all attributes are set."""
        logger.debug("Model post init")

        if self.team:
            logger.warning("Replacing team. TeamLead session_id: %s", self.session_id)

        # The context is passed automatically by Pydantic
        # We use self.user_id and self.session_id since they would have been set by Pydantic
        self.team = get_mitigator_team(
            user_id=self.user_id,
            session_id=self.session_id,
            model=get_gemini_pri_model(),
        )

    async def arun_stream(self, message: str) -> AsyncIterator[str]:
        error_data = {"error": "Invalid input: message must be a non-empty string"}

        if not message or not isinstance(message, str):
            yield ujson.dumps({"event": "error", "data": error_data})
            return

        yield ujson.dumps({"event": "start", "data": ""})

        try:
            response_stream: AsyncIterator[TeamRunResponse] = await self.team.arun(  # type: ignore
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
            yield ujson.dumps({"event": "cancelled", "data": {"content": str(e)}})
            return

        # except Exception as e:
        #     logger.error("team_lead_b: %s", e)
        #     error_details = {"error": str(e), "type": type(e).__name__}
        #     yield ujson.dumps({"event": "error", "data": error_details})

        finally:
            yield ujson.dumps({"event": "end", "data": ""})

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            Team: lambda v: None,
            # Agent: lambda v: None,
            # Storage: lambda v: None,
            # RecursiveChunking: lambda v: None,
            # MemoryDb: lambda v: None,
            # PgMemoryDb: lambda v: None,
            # TeamMemory: lambda v: None,
            # AgentMemory: lambda v: None
        },
    )


async def create_teamlead(user_id: str, session_id: str) -> TeamLead:
    logger.debug("Creating teamlead: %s", session_id)

    teamlead = TeamLead(user_id=user_id, session_id=session_id)

    return teamlead
