import asyncio
import json
from typing import Any, AsyncGenerator, AsyncIterator, Dict, Union

from agno.run.team import TeamRunResponse
from agno.team.team import Team
from agno.utils.log import logger
from pydantic import BaseModel

from config import config
from llmx.agent import get_agent
from llmx.agent_memory import get_team_memory
from llmx.models import gemini_model, or_gemini2_flash
from llmx.storage_db import get_storage

mitigator_team = Team(
    name="Mitigator Assistant Team Lead",
    mode="route",
    # mode="collaborate",
    team_id="massist_team",
    user_id="stolyarchuk",
    # reasoning=True,
    model=gemini_model,
    members=[
        get_agent("install", "Installation"),
        get_agent("integrate", "Integration"),
        get_agent("versions", "Versions"),
        get_agent("maintenance", "Maintenance"),
        get_agent("kb", "Knowledge Base"),
        get_agent("psg", "PCAP Signature Generator"),
        get_agent("contact", "Support"),
        get_agent("price", "Price"),
    ],
    storage=get_storage('ceo'),
    memory=get_team_memory('ceo'),
    instructions=[
        "You are the lead customer support agent responsible for classifying and routing customer inquiries.",
        # "Carefully analyze each user message, review main topics and it then route them to appropriate agents.",
        "Route customer question to appropriate agents. If no appropriate agent found think again.",
        "Release notes questions route to versions agent.",
        "For version informationm updates and changelogs route query to versions agent.",
        "Tech support questions decompose first and the route to appropriate agents. Always route to install agent.",
        "Setup and configure related questions route to knowledge base agent primary.",
        "After receiving responses from agents, combine and summarize them into a single, compehensive response.",
        "Then relay that information back to the user in a professional and helpful manner.",
        "Ensure a seamless experience for the user by maintaining context throughout the conversation.",
        # "Never disclose your team and agents information. Always give an abstract answer in questions related to your team."
    ],
    # success_criteria="The team has reached a consensus.",
    # update_team_context=True,
    # send_team_context_to_members=True,
    show_tool_calls=config.AGENT_SHOW_TOOL_CALLS,
    markdown=config.AGENT_MARKDOWN,
    debug_mode=config.TEAM_DEBUG,
    show_members_responses=True,
    enable_team_history=True,
    enable_agentic_context=True,
)


class Lead:
    """
    Lead class that holds and manages access to the Mitigator team.

    This class provides a wrapper around team operations and ensures
    responses are properly formatted for streaming.
    """
    mitigator_team: Team = mitigator_team

    async def run_stream(self, user_input: str, **kwargs) -> AsyncGenerator[str, None]:
        """
        Wrapper for mitigator_team.run that returns a valid StreamSSE format.

        Args:
            user_input: The user's query or input message
            **kwargs: Additional arguments to pass to the team's run method

        Yields:
            JSON formatted strings compatible with StreamSSE
        """
        if not user_input or not isinstance(user_input, str):
            yield json.dumps({"event": "error", "data": {"error": "Invalid input: user_input must be a non-empty string"}})
            return

        # Initial event indicating stream start
        yield json.dumps({"event": "start", "data": ""})

        # Ensure stream is set to True regardless of what's in kwargs
        # kwargs['stream'] = True
        # stream_intermediate_steps

        try:
            response_stream: AsyncIterator[TeamRunResponse] = await self.mitigator_team.arun(  # type: ignore
                message=user_input, stream_intermediate_steps=True, stream=True
            )

            async for chunk in response_stream:  # type: ignore
                if not chunk:  # Skip empty chunks
                    continue

                if isinstance(chunk, dict):
                    # For structured data responses
                    yield json.dumps({"event": "message", "data": chunk.to_dict()})
                elif isinstance(chunk, str):
                    # For text chunks, ensure they're properly formatted
                    yield json.dumps({"event": "message", "data": chunk.to_dict()})
                else:
                    # Convert any other type to string representation
                    yield json.dumps({"event": "message", "data": chunk.to_dict()})

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

    async def run(self, user_input: str, **kwargs) -> Dict[str, Any]:
        """
        Non-streaming wrapper for mitigator_team.run

        Args:
            user_input: The user's query or input message
            **kwargs: Additional arguments to pass to the team's run method

        Returns:
            Complete response from the team

        Raises:
            ValueError: If user_input is empty or not a string
            Exception: Any exception that might occur during team execution
        """
        if not user_input or not isinstance(user_input, str):
            raise ValueError(
                "Invalid input: user_input must be a non-empty string")

        # Ensure stream is set to False
        kwargs['stream'] = False

        try:
            return await self.mitigator_team.arun(user_input, **kwargs)
        except Exception as e:
            logger.error(e)
            raise


multi_language_team = Team(
    name="Multi Language Team",
    mode="route",
    user_id="stolyarchuk",
    model=gemini_model,
    members=[
        # english_agent,
        # spanish_agent,
        # japanese_agent,
        # french_agent,
        # german_agent,
        # chinese_agent,
    ],
    show_tool_calls=True,
    storage=get_storage('ceo'),
    memory=get_team_memory('ceo'),
    markdown=True,
    instructions=[
        "You are a language router that directs questions to the appropriate language agent.",
        "If the user asks in a language whose agent is not a team member, respond in English with:",
        "'I can only answer in the following languages: English, Spanish, Japanese, " +
        "French and German. Please ask your question in one of these languages.'",
        "Always check the language of the user's input before routing to an agent.",
        "For unsupported languages like Italian, respond in English with the above message.",
    ],
    show_members_responses=True,
    enable_team_history=True,
)

# Create a default lead instance for easy import
lead = Lead()
