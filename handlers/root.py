import asyncio

from aiogram import F, Router, html
from aiogram.enums import MessageEntityType
from aiogram.filters import CommandStart
from aiogram.types import Chat, Message

from filters.chat_type import ChatType

# from massist.agent import get_agent
from massist.logger import get_logger
from middlewares.long_operation import LongOperation

logger = get_logger(__name__)

router = Router()  # [1]

router.message.middleware(LongOperation())


@router.message(F.entities[:].type == MessageEntityType.EMAIL)
async def all_emails(message: Message):
    await message.answer("All entities are emails")


@router.message(F.entities[...].type == MessageEntityType.EMAIL)
async def any_emails(message: Message):
    await message.answer("At least one email!")


@router.message(
    ChatType(chat_type=["group", "supergroup"]),
    CommandStart(),
    flags={"long_operation": "typing"},
)
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """

    logger.debug(message.chat)

    if message.from_user is None:
        full_name = "Guest"
    else:
        # get_punk_agent("cyber_cyxap", str(message.from_user.id))

        full_name = message.from_user.first_name
        full_name += (
            f" {message.from_user.last_name}" if message.from_user.last_name else ""
        )

    await asyncio.sleep(2)

    await message.answer(f"Hello, {html.bold(full_name)}!")


@router.message(F.text, flags={"long_operation": "typing"})
async def greet_alice(message: Message) -> None:
    if message.from_user is None:
        return

    logger.debug(message.chat)

    # if message.entities:
    #     for entity in message.entities:
    #         if entity.type == "mention" and message.text:
    #             mentioned_username = message.text[
    #                 entity.offset : entity.offset + entity.length
    #             ]

    #             if "cyber_cyxap" in mentioned_username:
    #                 return

    # punk = get_punk_agent("cyber_cyxap", str(message.from_user.id))

    # reply = await punk.arun(message.text)

    await asyncio.sleep(4)

    await message.answer(
        "reply.content", parse_mode="HTML", disable_web_page_preview=True
    )


@router.message(F.forward_from_chat[F.type == "channel"].as_("channel"))
async def forwarded_from_channel(message: Message, channel: Chat):
    logger.debug(message.chat)

    await message.answer(f"This channel's ID is {channel.id}")
