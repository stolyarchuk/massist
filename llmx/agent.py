from typing import Any, Dict

from agno.agent.agent import Agent
from agno.models.base import Model
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel, ConfigDict

from config import config
from llmx.agent_memory import get_agent_memory
from llmx.knowledge import get_kb
from llmx.meta import Meta
from llmx.models import get_google_model, get_openrouter_model
from llmx.storage_db import get_storage


class AgentParams(BaseModel):
    session_id: str
    user_id: str
    model: Model
    memory_model: Model

    model_config = ConfigDict(arbitrary_types_allowed=True)


def get_agent(agent_id: str, topic: str, params: AgentParams):
    meta = Meta(agent_id=agent_id, topic=topic)
    # FIXME: remove default stolyarchuk

    return Agent(
        name=f"Mitigator {topic} Assistant",
        agent_id=f"mitigator_assistant_{agent_id}",
        role=meta.role,
        user_id=params.user_id,
        session_id=params.session_id,
        model=params.model,
        knowledge=get_kb(agent_id, model=get_openrouter_model()),
        search_knowledge=True,
        storage=get_storage(agent_id),
        memory=get_agent_memory(
            agent_id=agent_id, user_id=params.user_id, model=params.memory_model),
        description=meta.description,
        instructions=meta.instructions,
        read_chat_history=True,
        add_name_to_instructions=True,
        tools=[DuckDuckGoTools()],
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        read_tool_call_history=True,
        num_history_responses=3,
        markdown=config.AGENT_MARKDOWN,
        show_tool_calls=config.AGENT_SHOW_TOOL_CALLS,
        stream=config.AGENT_STREAM,
        debug_mode=config.AGENT_DEBUG,
        monitoring=config.AGENT_MONITORING
    )


def get_search_agent(agent_id: str, topic: str, params: AgentParams):
    meta = Meta(agent_id=agent_id, topic=topic)

    return Agent(
        name=f"Mitigator {topic} Assistant",
        agent_id=f"mitigator_assistant_{agent_id}",
        role=meta.role,
        user_id=params.user_id,
        session_id=params.session_id,
        model=params.model,
        # knowledge=get_kb(agent_id),
        # search_knowledge=True,
        add_references=True,
        storage=get_storage(agent_id),
        memory=get_agent_memory(
            agent_id=agent_id, user_id=params.user_id, model=get_openrouter_model()),
        description="You are a Web Researcher",
        instructions=meta.instructions,
        read_chat_history=True,
        add_name_to_instructions=True,
        tools=[DuckDuckGoTools()],
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        read_tool_call_history=True,
        num_history_responses=3,
        markdown=config.AGENT_MARKDOWN,
        show_tool_calls=config.AGENT_SHOW_TOOL_CALLS,
        stream=config.AGENT_STREAM,
        debug_mode=config.AGENT_DEBUG,
        monitoring=config.AGENT_MONITORING
    )
