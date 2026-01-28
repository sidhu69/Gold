from aiogram import types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from keyboards import main_menu
from config import CHANNEL_USERNAME
from helpers import is_member

def register(dp, bot):

    @dp.message(CommandStart())
    async def start(message: types.Message):
        if not await is_member(bot, message.from_user.id):
            kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="Join Channel",
                    url=f"https://t.me/{CHANNEL_USERNAME}"
                )],
                [InlineKeyboardButton(
                    text="Confirm",
                    callback_data="check_join"
                )]
            ])
            await message.answer("🚫 Join channel to use bot", reply_markup=kb)
            return

        await message.answer("Welcome to A Wallet 💎", reply_markup=main_menu())

    @dp.callback_query(lambda c: c.data == "check_join")
    async def confirm_join(query: CallbackQuery):
        if await is_member(bot, query.from_user.id):
            await query.message.answer("✅ Access granted", reply_markup=main_menu())
        else:
            await query.answer("Join channel first!", show_alert=True)
