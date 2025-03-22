from agno.agent.agent import Agent
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools

from config import config
from llmx.knowledge import knowledge_base
from llmx.meta import meta
from llmx.models import google_model
from llmx.storage import sqlite_storage

mitigator_assistant = Agent(
    name="Mitigator Assistant",
    agent_id="mitigator_assistant",
    # session_id="e8942e20-4fb9-4d0d-8fce-937f14b681d7",
    user_id="stolyarchuk",
    # model=OpenAIChat(api_key=settings.OPENAI_API_KEY.get_secret_value()),
    model=google_model,
    knowledge=knowledge_base,
    search_knowledge=True,
    storage=sqlite_storage,
    description=meta.description,
    instructions=meta.instructions,
    read_chat_history=True,  # This setting gives the model a tool to get chat history
    tools=[DuckDuckGoTools()],
    # This setting tellss the model to format messages in markdown
    markdown=config.AGENT_MARKDOWN,
    show_tool_calls=False,
    add_history_to_messages=True,
    add_datetime_to_instructions=True,
    read_tool_call_history=True,
    num_history_responses=3,
    stream=False,
    debug_mode=False,
)
