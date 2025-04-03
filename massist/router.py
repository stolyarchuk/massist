from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi.responses import UJSONResponse
from pydantic import BaseModel
from redis.asyncio.client import Redis
from sse_starlette.sse import EventSourceResponse

from massist import team_lead
from massist.logger import logger
from massist.redis import get_rdb
from massist.storage_db import get_storage
from massist.team_lead import TeamLead, cache_user_profile, get_cached_profile


class ChatIn(BaseModel):
    message: str


class MessageResponse(BaseModel):
    role: str
    content: str
    # id: str
    # session_id: str
    # created_at: str


async def create_chat(session_id: str):
    team_lead = TeamLead(user_id="stolyarchuk", session_id=session_id)

    if not await cache_user_profile(team_lead):
        logger.error("Failed to serialize TeamLead: %s",
                     team_lead.model_dump())

    return team_lead

# Get Redis db dependency


router = APIRouter()


@router.head('/health')
@router.get('/health')
def health_check():
    return UJSONResponse({'status': "healthy"})


@router.post('/chat/new')
async def single_chat(rdb: Redis = Depends(get_rdb)):
    chat_id = str(uuid4())
    # created = int(time())
    # await create_chat(rdb, chat_id, created)
    # cache = RedisCache(rdb, prefix="items")
    await create_chat(session_id=chat_id)
    return UJSONResponse({'chat_id': chat_id})


@router.post('/chat/{chat_id}')
async def chat(chat_id: str, chat_in: ChatIn):
    logger.debug("chat_id: %s, message: %s", chat_id, chat_in.message)

    team_lead = await get_cached_profile(session_id=chat_id)

    print("team_lead", team_lead)

    if team_lead is None:
        team_lead = await create_chat(session_id=chat_id)

    # lead = TeamLead(user_id="stolyarchuk", session_id=chat_id)

    return EventSourceResponse(
        content=team_lead.arun_stream(  # type: ignore
            message=chat_in.message
        )
    )


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
