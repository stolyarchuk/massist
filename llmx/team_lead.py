import asyncio
import json
from typing import Any, AsyncGenerator, AsyncIterator, Dict

from agno.run.team import TeamRunResponse
from agno.team.team import Team
from agno.utils.log import logger
from pydantic import BaseModel

from llmx.models import gemini2_model, gemini_model
from llmx.team import get_mitigator_team


class TeamLead(BaseModel):
    """
    Lead class that holds and manages access to the Mitigator team.

    This class provides a wrapper around team operations and ensures
    responses are properly formatted for streaming.
    """
    user_id: str = ""
    session_id: str = ""

    mitigator_team: Team = get_mitigator_team(
        user_id=user_id,
        session_id=session_id,
        model=gemini_model,
        memory_model=gemini2_model
    )

    async def arun_stream(self, message: str) -> AsyncIterator[str] | None:
        error_data = {
            "error": "Invalid input: message must be a non-empty string"}

        if not message or not isinstance(message, str):

            yield json.dumps({"event": "error", "data": error_data})
            return

        # Initial event indicating stream start
        yield json.dumps({"event": "start", "data": ""})

        try:
            response_stream: AsyncIterator[TeamRunResponse] = await self.mitigator_team.arun(  # type: ignore
                message=message, stream_intermediate_steps=True, stream=True
            )

            # return response_stream

            async for chunk in response_stream:  # type: ignore
                if not chunk:  # Skip empty chunks
                    continue

                if isinstance(chunk, dict):
                    # For structured data responses
                    yield json.dumps({"event": "message", "data": chunk})
                elif isinstance(chunk, TeamRunResponse):
                    # For text chunks, ensure they're properly formatted
                    yield json.dumps({"event": "message", "data": chunk.to_dict()})
                else:
                    # Convert any other type to string representation
                    yield json.dumps({"event": "message", "data": chunk})

        except asyncio.CancelledError:
            # Handle client disconnection gracefully
            yield json.dumps({"event": "cancelled", "data": {"message": "Stream cancelled"}})
            return

        except Exception as e:
            # More detailed error information
            error_details = {
                "error": str(e),
                "type": type(e).__name__
            }
            yield json.dumps({"event": "error", "data": error_details})

        finally:
            # Final event indicating stream completion
            yield json.dumps({"event": "end", "data": ""})

    async def arun(self, message: str) -> TeamRunResponse:
        if not message or not isinstance(message, str):
            raise ValueError(
                "Invalid input: user_input must be a non-empty string")

        try:
            return await self.mitigator_team.arun(message=message, stream=False, stream_intermediate_steps=False)
        except Exception as e:
            logger.error(e)
            raise


# Create a default lead instance for easy import
lead = TeamLead()
