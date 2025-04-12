import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from handlers import root, usernames
from massist.logger import get_logger

logger = get_logger(__name__)


# Запуск бота
async def start_bot():
    bot = Bot(
        token=config.TGBOT_API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_routers(root.router, usernames.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, handle_signals=False)


async def start_bot_nonblock():
    bot = Bot(
        token=config.TGBOT_API_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_routers(root.router)

    await bot.delete_webhook(drop_pending_updates=True)

    asyncio.ensure_future(
        dp.start_polling(bot, handle_signals=False), loop=asyncio.get_event_loop()
    )

    return dp

    # await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info(config.TGBOT_API_TOKEN)
    asyncio.run(start_bot())
