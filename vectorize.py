from massist.knowledge import get_kb
from massist.logger import init_logging
from massist.models import (get_gemini_pri_model, get_mistral_model,
                            get_openrouter_model)

init_logging()

if __name__ == "__main__":
    chunking_model = get_mistral_model(temperature=0.6)

    get_kb(topic="install", model=get_gemini_pri_model()).load(
        recreate=True, upsert=True
    )
    # get_kb(topic="integrate").load(recreate=True, upsert=True)
    # get_kb(topic="versions").load(recreate=True, upsert=True)
    # get_kb(topic="maintenance").load(recreate=True, upsert=True)
    # get_kb(topic="kb").load(recreate=True, upsert=True)
    # get_kb(topic="psg").load(recreate=True, upsert=True)
    # get_kb(topic="contact").load(recreate=True, upsert=True)
    # get_kb(topic="price").load(recreate=True, upsert=True)
    # get_kb(topic="collector").load(recreate=True, upsert=True)
    # pass
