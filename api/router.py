from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi.responses import UJSONResponse
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from db.redis import RedisAsyncPool
from massist.auth import verify_token
from massist.helpers import get_team_lead
from massist.logger import get_logger

# from massist.team_lead import TeamLead, create_teamlead

logger = get_logger(__name__)


async def get_rdb():
    rdb = RedisAsyncPool()
    try:
        yield rdb
    finally:
        await rdb.aclose()


class ChatIn(BaseModel):
    message: str


class MessageResponse(BaseModel):
    role: str
    content: str
    # id: str
    # session_id: str
    # created_at: str


router = APIRouter()


@router.get("/health", tags=["Public"])
async def health_check():
    return UJSONResponse({"status": "healthy"})


@router.get("/status", tags=["Protected"], dependencies=[Depends(verify_token)])
async def status_check():
    return UJSONResponse({"status": "healthy"})


@router.post("/chat/new", tags=["Protected"], dependencies=[Depends(verify_token)])
async def create_chat(pool: RedisAsyncPool = Depends(get_rdb)):
    session_id = str(uuid4())
    # created = int(time())
    # await create_chat(rdb, chat_id, created)
    # cache = RedisCache(rdb, prefix="items")
    teamlead = await get_team_lead(
        user_id="massist_web", session_id=session_id, pool=pool
    )

    logger.info("Chat created: %s", teamlead.session_id)
    logger.debug("Created new chat with ID: %s", session_id)

    return UJSONResponse({"chat_id": session_id})


@router.post(
    "/chat/{chat_id}", tags=["Protected"], dependencies=[Depends(verify_token)]
)
async def chat(chat_id: str, chat_in: ChatIn, pool: RedisAsyncPool = Depends(get_rdb)):
    logger.debug("chat_id: %s, message: %s", chat_id, chat_in.message)

    teamlead = await get_team_lead(user_id="massist_web", session_id=chat_id, pool=pool)

    return EventSourceResponse(content=teamlead.arun_stream(message=chat_in.message))


# @router.get(
#     '/messages/{chat_id}',
#     response_model=List[MessageResponse],
#     # tags=["Protected"],
#     # dependencies=[Depends(verify_token)]
# )
# async def get_messages(chat_id: str):
#     logger.warning("Retrieving messages for chat_id: %s", chat_id)

#     sessions = get_storage("lead").get_all_sessions()
#     messages: List[MessageResponse] = []
#     # current_session = None

#     for session in sessions:
#         logger.error("Session: %s", session)
#         if (
#             session.session_id == chat_id
#             and session.memory is not None
#             and len(session.memory['messages']) > 0
#         ):
#             messages = session.memory['messages']

#     # logger.warning("messages %s", messages.)

#     for message in messages:
#         logger.info("message %s", message)

#     return UJSONResponse([MessageResponse(**message).model_dump_json() for message in messages])
