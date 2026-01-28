from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from callbacks import MainCB
from config import CHANNEL_USERNAME

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💰 Buy Gold",
            callback_data=MainCB(action="buy").pack()
        )],
        [InlineKeyboardButton(
            text="📊 Prices",
            callback_data=MainCB(action="prices").pack()
        )],
        [InlineKeyboardButton(
            text="📢 Channel",
            url=f"https://t.me/{CHANNEL_USERNAME}"
        )]
    ])
