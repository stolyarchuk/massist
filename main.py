import asyncio

from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app

from llmx.agents import get_agent, mitigator_team
from llmx.logger import init_logging

init_logging()

# app = Playground(agents=mitigator_team.members).get_app()  # type: ignore
app = Playground(agents=[get_agent(1024)]).get_app()  # type: ignore

if __name__ == "__main__":
    serve_playground_app("main:app", reload=True)

    # asyncio.run(
    #     mitigator_team.print_response(
    #         message="Начните рассуждения на тему интеграция митигатора с внешними системами'",
    #         stream=True,
    #         stream_intermediate_steps=True,
    #     )
    # )
