import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import config
from llmx.api import router
from llmx.logger import init_logging

init_logging()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router)


@app.head('/health')
@app.get('/health')
def health_check():
    return 'ok'


uvicorn.run(app=app, reload=False)
