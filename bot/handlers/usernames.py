from typing import List

from aiogram import F, Router
from aiogram.types import Message

from bot.filters.has_usernames import HasUsernames

router = Router()


@router.message(F.text, HasUsernames())
async def message_with_usernames(message: Message, usernames: List[str]):
    await message.reply(f"{', '.join(usernames)}")
