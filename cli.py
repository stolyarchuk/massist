import asyncio

from config import config
# from massist.logger import init_logging
from massist.models import get_google_model
from massist.team import get_mitigator_team

# init_logging()


if __name__ == "__main__":
    # mitigator_team = get_mitigator_team(
    #     user_id="user_id",
    #     session_id="session_id",
    #     model=get_google_model(model_id=config.GEMINI_MODEL_PRI),
    #     memory_model=get_google_model(model_id=config.GEMINI_MODEL_SEC)
    # )

    # asyncio.run(
    #     mitigator_team.aprint_response(  # type: ignore
    #         # message="расскажи про себя и свою команду.",
    #         # message="расскажи про все изменения в последней версии митигатора.",
    #         message="как установить и быстро настроить защиту в митигаторе?",
    #         # message="какие системные требования?",
    #         # message="как настроить ISN?.",
    #         # message="что нового появилось в митигаторе в этом году?.",
    #         stream=True,
    #         stream_intermediate_steps=True,
    #     )
    # )
    pass
