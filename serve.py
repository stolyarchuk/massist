import asyncio

import uvicorn
from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app
from fastapi import FastAPI

from llmx.agent_teams import mitigator_team
from llmx.logger import init_logging

app = FastAPI()

init_logging()


@app.get("/ask")
async def ask(query: str):
    response = await mitigator_team.arun(query, stream=False)
    return {"response": response.content}


# app = Playground(agents=mitigator_team).get_app()  # type: ignore
# app = Playground(agents=[agent_id(1024)]).get_app()  # type: ignore

if __name__ == "__main__":
    uvicorn.run(app=app)
    # serve_playground_app("main:app", reload=True)

    # asyncio.run(
    #     mitigator_team.print_response(
    #         message="Начните рассуждения на тему интеграция митигатора с внешними системами'",
    #         stream=True,
    #         stream_intermediate_steps=True,
    #     )
    # )
