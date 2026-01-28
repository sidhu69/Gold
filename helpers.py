from aiogram.exceptions import TelegramAPIError
from config import CHANNEL_ID

async def is_member(bot, user_id: int) -> bool:
    try:
        m = await bot.get_chat_member(CHANNEL_ID, user_id)
        return m.status in ("member", "administrator", "creator")
    except TelegramAPIError:
        return False
