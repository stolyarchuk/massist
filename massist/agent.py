from typing import Any, List

from agno.agent.agent import Agent
from agno.models.base import Model
from agno.storage.base import Storage
from agno.tools.dalle import DalleTools
from agno.tools.duckduckgo import DuckDuckGoTools
from pydantic import BaseModel, ConfigDict

from config import config
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
    storage: Storage | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


def get_agent(
    agent_id: str, topic: str, params: AgentParams, tools: List[Any] | None = None
):
    meta = Meta(agent_id=agent_id, topic=topic)
    if tools is None:
        tools = [
            DuckDuckGoTools(),
        ]

    return Agent(
        name=f"AI {topic} Agent",
        agent_id=f"{agent_id}_agent",
        role=meta.role,
        user_id=params.user_id,
        session_id=params.session_id,
        model=params.model,
        knowledge=get_kb(topic=agent_id, chunking_model=get_openrouter_model()),
        search_knowledge=True,
        storage=params.storage,
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
        enable_user_memories=config.AGENT_ENABLE_USER_MEMORIES,
        enable_session_summaries=config.AGENT_ENABLE_SESSION_SUMMARIES,
        telemetry=False,
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
        name=f"AI {topic} Agent",
        agent_id=f"{agent_id}_agent",
        role=meta.role,
        user_id=params.user_id,
        session_id=params.session_id,
        model=params.model,
        # knowledge=get_kb(agent_id),
        # search_knowledge=True,
        add_references=True,
        storage=params.storage,
        memory=get_agent_memory(
            agent_id=agent_id,
            user_id=params.user_id,
            manager_model=get_gemini_pri_model(),
            classifier_model=get_gemini_sec_model(),
            summarizer_model=get_gemini_sec_model(),
        ),
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
        respond_directly=False,
    )


def get_image_agent(
    agent_id: str, topic: str, params: AgentParams, tools: List[Any] | None = None
):
    # meta = Meta(agent_id=agent_id, topic="Image")

    if tools is None:
        tools = [
            DalleTools(api_key=config.OPENAI_API_KEY),
        ]

    return Agent(
        name=f"AI {topic} Agent",
        agent_id=f"{agent_id}_agent",
        role="Image Generator",
        user_id=params.user_id,
        session_id=params.session_id,
        model=params.model,
        # knowledge=get_kb(
        #     topic=agent_id, chunking_model=get_openrouter_model()),
        # search_knowledge=True,
        storage=params.storage,
        memory=get_agent_memory(
            agent_id=agent_id,
            user_id=params.user_id,
            manager_model=get_gemini_pri_model(),
            classifier_model=get_gemini_sec_model(),
            summarizer_model=get_gemini_sec_model(),
        ),
        description="You are an AI agent that can generate images using DALL-E.",
        instructions=[
            "When you are asked to create an image, use the `create_image` tool to create the image.",
            "The DALL-E tool will return an image URL.",
            "Return the image URL in your response in the following format: `![image description](image URL)`",
        ],
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
