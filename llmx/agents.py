from agno.agent.agent import Agent
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools

from config import config
from llmx.knowledge import get_kb
from llmx.meta import meta
from llmx.models import google_model
from llmx.storage import get_storage


def get_agent(num: int):
    return Agent(
        name=f"Mitigator Assistant {num}",
        agent_id=f"mitigator_assistant_{num}",
        user_id="stolyarchuk",
        model=google_model,
        knowledge=get_kb(num),
        search_knowledge=True,
        storage=get_storage(num),
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


mitigator_team = Team(
    name="Discussion Team",
    mode="collaborate",
    model=google_model,
    members=[
        get_agent(1024),
        get_agent(768),
        get_agent(896),
    ],
    instructions=[
        "You are a discussion master.",
        "You have to stop the discussion when you think the team has reached a consensus.",
    ],
    success_criteria="The team has reached a consensus.",
    # update_team_context=True,
    # send_team_context_to_members=True,
    show_tool_calls=True,
    markdown=True,
    show_members_responses=True,
)
