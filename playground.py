from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app  # type: ignore

from config import config
from massist.logger import init_logging
from massist.models import get_google_model
from massist.team import get_mitigator_team

# init_logging()

mitigator_team = get_mitigator_team(
    user_id="stolyarchuk",
    session_id="",
    model=get_google_model(model_id=config.GEMINI_MODEL_PRI),
    memory_model=get_google_model(model_id=config.GEMINI_MODEL_SEC)
)

app = Playground(agents=mitigator_team.members).get_app()  # type: ignore

if __name__ == "__main__":
    serve_playground_app("main:app", reload=False)
