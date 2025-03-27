import asyncio
from typing import Any, AsyncGenerator, AsyncIterator, Iterator

import ujson
from agno.run.team import TeamRunResponse
from agno.team.team import Team
from pydantic import BaseModel, ConfigDict

from llmx.logger import logger
from llmx.models import gemini2_model, gemini_model
from llmx.team import get_mitigator_team


# class TeamLead(BaseModel):
class TeamLead:
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # user_id: str = ""
    # session_id: str = ""

    user_id: str = "stolyarchuk"
    session_id: str = "c58dcf27-faa9-43cf-b007-f752f4c4e001"

    mitigator_team: Team = get_mitigator_team(
        user_id=user_id,
        session_id=session_id,
        model=gemini_model,
        memory_model=gemini2_model
    )

    async def arun_stream(self, message: str) -> AsyncGenerator:
        error_data = {
            "error": "Invalid input: message must be a non-empty string"}

        if not message or not isinstance(message, str):

            yield ujson.dumps({"event": "error", "data": error_data})
            return

        # Initial event indicating stream start
        yield ujson.dumps({"event": "start", "data": ""})

        try:
            response_stream: Any = await self.mitigator_team.arun(  # type: ignore
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
            logger.warning(e)
            yield ujson.dumps({"event": "cancelled", "data": {"content": "Stream cancelled"}})
            return

        except Exception as e:
            logger.error(e)
            error_details = {
                "error": str(e),
                "type": type(e).__name__
            }
            yield ujson.dumps({"event": "error", "data": error_details})

        finally:
            yield ujson.dumps({"event": "end", "data": ""})

    # async def arun(self, message: str) -> TeamRunResponse:
    #     if not message or not isinstance(message, str):
    #         raise ValueError(
    #             "Invalid input: user_input must be a non-empty string")

    #     try:
    #         response: TeamRunResponse = await self.mitigator_team.arun(  # type: ignore
    #             message=message, stream=False, stream_intermediate_steps=False
    #         )
    #         return response
    #     except Exception as e:
    #         logger.error(e)
    #         raise
