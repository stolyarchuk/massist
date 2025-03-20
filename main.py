import logging

from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app
from dotenv import load_dotenv

from llmx.agents import mitigator_assistant

load_dotenv()
# loggers = [logging.getLogger().name]
# loggers += list(logging.Logger.manager.loggerDict.keys())

loggers = [lg for lg in logging.Logger.manager.loggerDict.keys()]

# update_formatters(*loggers)
init_module_loggers(*loggers)


# mlinks = ['https://docs.mitigator.ru/v24.10/',
#           'https://docs.mitigator.ru/v24.10/install/',
#           'https://docs.mitigator.ru/v24.10/maintenance/',
#           'https://docs.mitigator.ru/v24.10/versions/',
#           'https://docs.mitigator.ru/v24.10/integrate/']


app = Playground(agents=[mitigator_assistant]).get_app()

if __name__ == "__main__":
    # knowledge_base.load(recreate=True, upsert=True)

    serve_playground_app("main:app", reload=True)
