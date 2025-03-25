from agno.agent.agent import Agent
from agno.models.base import Model
from agno.tools.duckduckgo import DuckDuckGoTools

from config import config
from llmx.agent_memory import get_agent_memory
from llmx.knowledge import get_kb
from llmx.meta import Meta
from llmx.models import gemini2_model, gemini_model
from llmx.storage_db import get_storage


def get_agent(agent_id: str, topic: str, model: Model = gemini_model):
    meta = Meta(agent_id=agent_id, topic=topic)

    return Agent(
        name=f"Mitigator Assistant in {topic}",
        agent_id=f"mitigator_assistant_{agent_id}",
        role=meta.role,
        user_id="stolyarchuk",
        model=model,
        knowledge=get_kb(agent_id),
        search_knowledge=True,
        storage=get_storage(agent_id),
        memory=get_agent_memory(agent_id, model=gemini2_model),
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
