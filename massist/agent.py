from typing import Any, List

from agno.agent.agent import Agent
from agno.models.base import Model
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel, ConfigDict

from massist.config import config
from massist.agent_memory import get_agent_memory
from massist.knowledge import get_kb
from massist.meta import Meta
from massist.models import (
    get_gemini_pri_model,
    get_gemini_sec_model,
    get_openrouter_model,
)


class AgentParams(BaseModel):
    session_id: str
    user_id: str
    model: Model

    model_config = ConfigDict(arbitrary_types_allowed=True)


def get_agent(
    agent_id: str, topic: str, params: AgentParams, tools: List[Any] | None = None
):
    meta = Meta(agent_id=agent_id, topic=topic)
    # FIXME: remove default stolyarchuk

    if tools is None:
        tools = [
            DuckDuckGoTools(),
        ]

    return Agent(
        name=f"Mitigator {topic} Agent",
        agent_id=f"mitigator_agent_{agent_id}",
        role=meta.role,
        user_id=params.user_id,
        session_id=params.session_id,
        model=params.model,
        knowledge=get_kb(topic=agent_id, chunking_model=get_openrouter_model()),
        search_knowledge=True,
        # storage=get_storage(agent_id),
        memory=get_agent_memory(
            agent_id=agent_id,
            user_id=params.user_id,
            manager_model=get_gemini_pri_model(),
            classifier_model=get_gemini_sec_model(),
            summarizer_model=get_gemini_sec_model(),
        ),
        description=meta.description,
        instructions=meta.instructions,
        read_chat_history=True,
        add_name_to_instructions=True,
        tools=tools,
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        read_tool_call_history=True,
        num_history_responses=3,
        markdown=config.AGENT_MARKDOWN,
        show_tool_calls=config.AGENT_SHOW_TOOL_CALLS,
        stream=config.AGENT_STREAM,
        debug_mode=config.AGENT_DEBUG,
        monitoring=config.AGENT_MONITORING,
    )


def get_search_agent(
    agent_id: str, topic: str, params: AgentParams, tools: List[Any] | None = None
):
    meta = Meta(agent_id=agent_id, topic=topic)
    # FIXME: remove default stolyarchuk

    if tools is None:
        tools = [
            DuckDuckGoTools(),
        ]

    return Agent(
        name=f"Mitigator {topic} Agent",
        agent_id=f"mitigator_agent_{agent_id}",
        role=meta.role,
        user_id=params.user_id,
        session_id=params.session_id,
        model=params.model,
        # knowledge=get_kb(agent_id),
        # search_knowledge=True,
        add_references=True,
        # storage=get_storage(agent_id),
        # memory=get_agent_memory(
        #     agent_id=agent_id,
        #     user_id=params.user_id,
        #     manager_model=get_gemini_pri_model(),
        #     classifier_model=get_gemini_sec_model(),
        #     summarizer_model=get_gemini_sec_model()
        # ),
        description="You are a Web Researcher",
        instructions=meta.instructions,
        read_chat_history=True,
        add_name_to_instructions=True,
        tools=tools,
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        read_tool_call_history=True,
        num_history_responses=3,
        markdown=config.AGENT_MARKDOWN,
        show_tool_calls=config.AGENT_SHOW_TOOL_CALLS,
        stream=config.AGENT_STREAM,
        debug_mode=config.AGENT_DEBUG,
        monitoring=config.AGENT_MONITORING,
    )
