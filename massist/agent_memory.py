from agno.memory.agent import AgentMemory
from agno.memory.classifier import MemoryClassifier
from agno.memory.manager import MemoryManager
from agno.memory.summarizer import MemorySummarizer
from agno.models.base import Model

from massist.memory import get_memory_db


def get_agent_memory(
    agent_id: str,
    user_id: str,
    manager_model: Model,
    classifier_model: Model,
    summarizer_model: Model,
) -> AgentMemory:
    return AgentMemory(
        user_id=user_id,
        db=get_memory_db(agent_id),
        create_user_memories=True,
        create_session_summary=True,
        manager=MemoryManager(model=manager_model),
        classifier=MemoryClassifier(model=classifier_model),
        summarizer=MemorySummarizer(model=summarizer_model),
    )
