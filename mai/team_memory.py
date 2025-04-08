from agno.memory.classifier import MemoryClassifier
from agno.memory.manager import MemoryManager
from agno.memory.team import TeamMemory
from agno.models.base import Model

from mai.memory import get_memory_db


def get_team_memory(
    agent_id: str, user_id: str, manager_model: Model, classifier_model: Model
) -> TeamMemory:
    return TeamMemory(
        user_id=user_id,
        db=get_memory_db(agent_id),
        create_user_memories=True,
        manager=MemoryManager(model=manager_model),
        classifier=MemoryClassifier(model=classifier_model),
    )
