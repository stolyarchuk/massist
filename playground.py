from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app  # type: ignore

from llmx.logger import init_logging
from llmx.team import mitigator_team

init_logging()

app = Playground(agents=mitigator_team.members).get_app()  # type: ignore

if __name__ == "__main__":
    serve_playground_app("main:app", reload=False)
