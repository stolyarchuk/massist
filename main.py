from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app

from llmx.agents import mitigator_assistant
from llmx.logger import init_logging

init_logging()

app = Playground(agents=[mitigator_assistant]).get_app()

if __name__ == "__main__":
    serve_playground_app("main:app", reload=True)
