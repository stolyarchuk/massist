import asyncio

from llmx.agent_teams import mitigator_team
from llmx.logger import init_logging

init_logging()


if __name__ == "__main__":
    asyncio.run(
        mitigator_team.aprint_response(
            message="расскажи про себя и свою команду.",
            # message="какая версия самая последняя? и расскажи про установку и быструю настройку.",
            # message="какие шаги надо выполнить для чек-листа настроек политик защиты.",
            # message="как настроить ISN?.",
            stream=False,
            stream_intermediate_steps=True,
        )
    )
