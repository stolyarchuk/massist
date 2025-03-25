from agno.team.team import Team

from config import config
from llmx.agent import get_agent
from llmx.agent_memory import get_team_memory
from llmx.models import gemini_model
from llmx.storage_db import get_storage

mitigator_team = Team(
    name="Mitigator Assistant Team",
    mode="route",
    # mode="collaborate",
    model=gemini_model,
    team_id="massist_team",
    user_id="stolyarchuk",
    members=[
        get_agent("install"),
        get_agent("integrate"),
        get_agent("versions"),
        get_agent("maintenance"),
        get_agent("kb"),
        get_agent("psg"),
        get_agent("contact"),
    ],
    storage=get_storage('ceo'),
    memory=get_team_memory('ceo'),
    instructions=[
        "You are the lead customer support agent responsible for classifying and routing customer inquiries.",
        # "Carefully analyze each user message, review main topics and it then route them to appropriate agents.",
        "Route customer question to appropriate agents. If no appropriate agent found think again.",
        "Setup and configure related questions route to kb agent primary.",
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
