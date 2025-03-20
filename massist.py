# Standard library imports
import logging
import sys
from textwrap import dedent

from agno.playground.playground import Playground
from agno.playground.serve import serve_playground_app
from agno.tools.duckduckgo import DuckDuckGoTools
# Third-party imports
from dotenv import load_dotenv

from config import config
from llmx.agents import mitigator_assistant
from logger import init_module_loggers, logger, update_formatters

# from agno.reranker.base import Reranker  # Unused import
# from agno.reranker.cohere import CohereReranker  # Unused import


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

    # knowledge_base.load(recreate=False, upsert=False)
    # knowledge_base.load(recreate=True, upsert=True)
    # kb.load(recreate=True, upsert=True)

    serve_playground_app("massist:app", reload=True)
