from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app

from llmx.agent_teams import mitigator_team
from llmx.logger import init_logging

init_logging()

app = Playground(agents=mitigator_team.members).get_app()  # type: ignore

if __name__ == "__main__":
    serve_playground_app("main:app", reload=False)
