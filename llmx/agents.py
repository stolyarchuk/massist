from agno.agent.agent import Agent
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools

from config import config
from llmx.knowledge import get_kb
from llmx.meta import meta
from llmx.models import google_model
from llmx.storage import get_storage


def get_agent(name: str):
    return Agent(
        name=f"Mitigator Assistant {name}",
        agent_id=f"mitigator_assistant_{name}",
        user_id="stolyarchuk",
        model=google_model,
        knowledge=get_kb(name),
        search_knowledge=True,
        storage=get_storage(name),
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
        get_agent("integrate"),
        # get_agent(768),
        # get_agent(896),
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


multi_language_team = Team(
    name="Multi Language Team",
    mode="route",
    model=google_model,
    members=[
        # english_agent,
        # spanish_agent,
        # japanese_agent,
        # french_agent,
        # german_agent,
        # chinese_agent,
    ],
    show_tool_calls=True,
    markdown=True,
    instructions=[
        "You are a language router that directs questions to the appropriate language agent.",
        "If the user asks in a language whose agent is not a team member, respond in English with:",
        "'I can only answer in the following languages: English, Spanish, Japanese, French and German. Please ask your question in one of these languages.'",
        "Always check the language of the user's input before routing to an agent.",
        "For unsupported languages like Italian, respond in English with the above message.",
    ],
    show_members_responses=True,
)
