import typer
from agno.agent.agent import Agent
from agno.models.deepseek.deepseek import DeepSeek

# from agno.models.openai.like import OpenAILike
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools

from settings import Settings

# from agno.models.openai.like import OpenAILike


# from openai import OpenAI


settings = Settings()

# client = OpenAI(
#     api_key=settings.OPENAI_API_KEY.get_secret_value(),
#     base_url=settings.OPENAI_BASE_URL,
# )

# models = client.models.list()
# model = models.data[0].id

# print(model)

# web_agent = Agent(
#     model=OpenAILike(
#         id="deepseek-chat",
#         api_key=settings.DEEPSEEK_API_KEY.get_secret_value(),
#         base_url=settings.OPENAI_BASE_URL,
#     ),
#     tools=[DuckDuckGoTools()],
#     show_tool_calls=settings.AGENT_SHOW_TOOL_CALLS,
#     markdown=settings.AGENT_MARKDOWN,
#     monitoring=True,
# )

web_agent = Agent(
    model=DeepSeek(id="deepseek-chat", api_key=settings.DEEPSEEK_API_KEY.get_secret_value()),
    tools=[DuckDuckGoTools()],
    show_tool_calls=settings.AGENT_SHOW_TOOL_CALLS,
    markdown=settings.AGENT_MARKDOWN,
)

# Round 1
# messages = [{"role": "user", "content": "9.11 and 9.8, which is greater?"}]
# response = client.chat.completions.create(model=model, messages=messages)

# reasoning_content = response.choices[0].message.reasoning_content
# content = response.choices[0].message.content

# print("reasoning_content:", reasoning_content)
# print("content:", content)

web_agent.print_response("Tell me about a breaking news story from New York.", stream=settings.AGENT_STREAM)
