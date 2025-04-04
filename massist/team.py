from textwrap import dedent

from agno.models.base import Model
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools

from config import config
from massist.agent import AgentParams, get_agent, get_search_agent
from massist.models import (get_gemini_pri_model, get_gemini_sec_model,
                            get_openrouter_model)
from massist.storage import get_storage
from massist.team_memory import get_team_memory


def get_mitigator_team(
    user_id: str,
    session_id: str,
    model: Model
) -> Team:

    def get_agent_params():
        return AgentParams(
            user_id=user_id,
            session_id=session_id,
            model=get_gemini_pri_model()
        )

    def get_tools():
        return DuckDuckGoTools()

    return Team(
        name="Mitigator AI Assistant",
        mode="route",
        team_id="massist_team",
        user_id=user_id,
        session_id=session_id,
        model=model,
        tools=[DuckDuckGoTools()],
        members=[
            get_agent("index", "Major", get_agent_params()),
            get_agent("install", "Installation", get_agent_params()),
            get_agent("integrate", "Integration", get_agent_params()),
            get_agent("versions", "Versions", get_agent_params()),
            get_agent("maintenance", "Maintenance", get_agent_params()),
            get_agent("kb", "Knowledge Base", get_agent_params()),
            get_agent("psg", "PCAP Signature Generator", get_agent_params()),
            get_agent("contact", "Support", get_agent_params()),
            get_agent("price", "Price", get_agent_params()),
            get_search_agent("web_search", "Web Search", get_agent_params())
        ],
        storage=get_storage('lead'),
        memory=get_team_memory(
            agent_id='lead',
            user_id=user_id,
            manager_model=get_gemini_pri_model(),
            classifier_model=get_gemini_sec_model()
        ),
        description=dedent("""
            You are the lead customer support team agent responsible for classifying and
            routing customer inquiries."""),
        instructions=[
            "Carefully analyze each customer message and then route it to appropriate agents.",
            # "Route customer question to appropriate agents. If no appropriate agenuser queryund think again.",
            # "Rewrite customer query and route to apropriate agents again.",
            "Release notes questions, version informationm updates and changelogs route to versions agent.",
            "Tech support questions decompose first and the route to appropriate agents.",
            "Setup and configure related questions route to knowledge base agent primary.",
            "Route query to all other agents at last.",
            "After receiving responses from agents, combine them into a single, compehensive response.",
            # "Route customer query to web_search agent if needed for comparison or if you didn't receive any " +
            # "answers from agents.",
            # "If no information provided from the agents, search customer query in the web " +
            # "with duckduckgo_search tool.",
            "Then relay that information back to the user in a professional and helpful manner.",
            "Always reply in russian language.",
            "Always disclose your team and agents information. Always give an abstract answer in questions " +
            "related to your team.",
            "Ensure a seamless experience for the user by maintaining context throughout the conversation.",
        ],
        # success_criteria="The team has reached a consensus.",
        # send_team_context_to_members=True,
        # reasoning=True,
        # reasoning_model=get_gemini_pri_model(),
        show_tool_calls=config.AGENT_SHOW_TOOL_CALLS,
        markdown=config.AGENT_MARKDOWN,
        debug_mode=config.TEAM_DEBUG,
        show_members_responses=True,
        enable_team_history=True,
        enable_agentic_context=True,
        telemetry=False,
    )


# def get_ml_team(user_id: str, model: Model) -> Team:
#     return Team(
#         name="Multi Language Team",
#         mode="route",
#         user_id=user_id,
#         model=model,
#         members=[
#             # english_agent,
#             # spanish_agent,
#             # japanese_agent,
#             # french_agent,
#             # german_agent,
#             # chinese_agent,
#         ],
#         show_tool_calls=True,
#         storage=get_storage(agent_id='ceo'),
#         memory=get_team_memory(
#             agent_id='ceo', user_id=user_id, model=get_openrouter_model()
#         ),
#         markdown=True,
#         instructions=[
#             "You are a language router that directs questions to the appropriate language agent.",
#             "If the user asks in a language whose agent is not a team member, respond in English with:",
#             "'I can only answer in the following languages: English, Spanish, Japanese, " +
#             "French and German. Please ask your question in one of these languages.'",
#             "Always check the language of the user's input before routing to an agent.",
#             "For unsupported languages like Italian, respond in English with the above message.",
#         ],
#         show_members_responses=True,
#         enable_team_history=True,
#     )
