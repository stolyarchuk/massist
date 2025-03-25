from agno.agent.agent import Agent
from agno.models.base import Model
from agno.tools.duckduckgo import DuckDuckGoTools

from config import config
from llmx.agent_memory import get_agent_memory
from llmx.knowledge import get_kb
from llmx.meta import meta
from llmx.models import gemini_model
from llmx.storage_db import get_storage


def get_agent(agent_id: str, model: Model = gemini_model):
    return Agent(
        name=f"Mitigator Assistant in {agent_id}",
        agent_id=f"mitigator_assistant_{agent_id}",
        user_id="stolyarchuk",
        model=model,
        knowledge=get_kb(agent_id),
        search_knowledge=True,
        storage=get_storage(agent_id),
        memory=get_agent_memory(agent_id),
        description=meta.description,
        instructions=meta.instructions,
        read_chat_history=True,
        add_name_to_instructions=True,
        tools=[DuckDuckGoTools()],
        markdown=config.AGENT_MARKDOWN,
        show_tool_calls=False,
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        read_tool_call_history=True,
        num_history_responses=3,
        stream=False,
        debug_mode=False,
        monitoring=True
    )
