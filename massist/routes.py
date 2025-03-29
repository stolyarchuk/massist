# from time import time
from uuid import uuid4

# from app.db import chat_exists, create_chat, get_redis
from fastapi import APIRouter
from fastapi.responses import UJSONResponse
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from massist.logger import logger
from massist.team_lead import TeamLead


class ChatIn(BaseModel):
    message: str

# Get Redis db dependency


router = APIRouter()


@router.head('/health')
@router.get('/health')
def health_check():
    return UJSONResponse({'status': "healthy"})


@router.post('/chat/new')
async def single_chat():
    chat_id = str(uuid4())
    # created = int(time())
    # await create_chat(rdb, chat_id, created)
    return UJSONResponse({'chat_id': chat_id})


@router.post('/chat/{chat_id}')
async def chat(chat_id: str, chat_in: ChatIn):
    logger.debug("chat_id: %s, message: %s", chat_id, chat_in.message)

    lead = TeamLead(user_id="stolyarchuk", session_id=chat_id)

    return EventSourceResponse(
        content=lead.arun_stream(  # type: ignore
            message=chat_in.message
        )
    )
