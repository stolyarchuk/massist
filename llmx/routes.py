from time import time
from uuid import uuid4

# from app.db import chat_exists, create_chat, get_redis
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from llmx.team_lead import lead


class ChatIn(BaseModel):
    message: str

# Get Redis db dependency


router = APIRouter()


@router.head('/health')
@router.get('/health')
def health_check():
    return {"status": "healthy"}


@router.post('/chat/new')
async def single_chat():
    chat_id = str(uuid4())
    created = int(time())
    # await create_chat(rdb, chat_id, created)
    return {'chat_id': chat_id}


# @router.post('/chats/{chat_id}')
@router.post('/chat/{chat_id}')
async def chat(chat_id: str, chat_in: ChatIn):
    # Dependencies with yield don't work with Streaming responses after version 0.106
    # So we are closing the Redis db connection with a background task
    # See issue: https://github.com/fastapi/fastapi/issues/11143
    # rdb = get_redis()
    # if not await chat_exists(rdb, chat_id):
    #     raise HTTPException(
    #         status_code=404, detail=f'Chat {chat_id} does not exist')
    sse_stream = await lead.arun_stream(message=chat_in.message)
    return EventSourceResponse(content=sse_stream)
