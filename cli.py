import asyncio

from llmx.agent_teams import mitigator_team
from llmx.logger import init_logging

init_logging()


if __name__ == "__main__":
    asyncio.run(
        mitigator_team.aprint_response(
            # message="расскажи про себя и свою команду.",
            message="расскажи про все изменения в последней версии v25.02.",
            # расскажи про установку и быструю настройку.",
            # message="какие шаги надо выполнить для чек-листа настроек политик защиты.",
            # message="как настроить ISN?.",
            # message="что нового появилось в митигаторе в этом году?.",
            stream=False,
            stream_intermediate_steps=True,
        )
    )
