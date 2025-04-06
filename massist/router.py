from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi.responses import UJSONResponse
from pydantic import BaseModel
from redis.asyncio.client import Redis
from sse_starlette.sse import EventSourceResponse

from massist.logger import get_logger
from massist.redis import get_rdb
from massist.team_lead import TeamLead, cache_teamlead, get_cached_teamlead

logger = get_logger(__name__)


class ChatIn(BaseModel):
    message: str


class MessageResponse(BaseModel):
    role: str
    content: str
    # id: str
    # session_id: str
    # created_at: str


async def create_chat(user_id: str, session_id: str, rdb: Redis) -> TeamLead:
    logger.debug("Creating chat session_id: %s", session_id)

    teamlead = TeamLead(user_id=user_id, session_id=session_id)
    # Use dict conversion instead of model_validate to avoid type errors
    # When creating an instance directly, model_validate is unnecessary

    return teamlead


router = APIRouter()


@router.head("/health")
@router.get("/health")
def health_check():
    return UJSONResponse({"status": "healthy"})


@router.post("/chat/new")
async def single_chat(rdb: Redis = Depends(get_rdb)):
    chat_id = str(uuid4())
    # created = int(time())
    # await create_chat(rdb, chat_id, created)
    # cache = RedisCache(rdb, prefix="items")
    teamlead = await create_chat(user_id="massist_buddy", session_id=chat_id, rdb=rdb)
    teamlead_cached = await cache_teamlead(teamlead, rdb=rdb)

    logger.info(
        "TeamLead created: %s. Cached: %s",
        teamlead.session_id,
        teamlead_cached
    )
    logger.debug("Created new chat with ID: %s", chat_id)

    return UJSONResponse({"chat_id": chat_id})


@router.post("/chat/{chat_id}")
async def chat(chat_id: str, chat_in: ChatIn, rdb: Redis = Depends(get_rdb)):
    logger.debug("chat_id: %s, message: %s", chat_id, chat_in.message)

    teamlead = await get_cached_teamlead(session_id=chat_id, rdb=rdb)

    if teamlead is None:
        teamlead = await create_chat(
            user_id="massist_buddy",
            session_id=chat_id,
            rdb=rdb
        )

        teamlead_cached = await cache_teamlead(teamlead, rdb=rdb)

        logger.info(
            "TeamLead created: %s. Cached: %s",
            teamlead.session_id,
            teamlead_cached
        )
    else:
        logger.debug("TeamLead fetched from cache: %s", teamlead.session_id)

    return EventSourceResponse(content=teamlead.arun_stream(message=chat_in.message))


# @router.get('/messages/{chat_id}', response_model=List[MessageResponse])
# async def get_messages(chat_id: str):
#     logger.warning("Retrieving messages for chat_id: %s", chat_id)

#     sessions = get_storage("lead").get_all_sessions()
#     messages: List[MessageResponse] = []
#     # current_session = None

#     for session in sessions:
#         if (
#             session.session_id == chat_id
#             and session.memory is not None
#             and len(session.memory['messages']) > 0
#         ):
#             messages = session.memory['messages']

#     logger.warning(messages)

#     return UJSONResponse([MessageResponse(**message).model_dump_json() for message in messages])
