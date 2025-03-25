from agno.team.team import Team

from llmx.agent import get_agent
from llmx.agent_memory import get_team_memory
from llmx.models import gemini_model
from llmx.storage_db import get_storage

mitigator_team = Team(
    name="Discussion Team",
    mode="collaborate",
    model=gemini_model,
    members=[
        get_agent("install"),
        get_agent("integrate"),
        get_agent("versions"),
        get_agent("maintenance"),
        # get_agent(768),
        # get_agent(896),
    ],
    storage=get_storage('ceo'),
    memory=get_team_memory('ceo'),
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
)
