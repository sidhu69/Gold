from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from callbacks import MainCB
from states import BuyState
from helpers import is_member
from config import GOLD_PRICE

def register(dp, bot):

    @dp.callback_query(MainCB.filter())
    async def main_router(query: CallbackQuery, callback_data: MainCB, state: FSMContext):
        if not await is_member(bot, query.from_user.id):
            await query.answer("Join channel first!", show_alert=True)
            return

        if callback_data.action == "buy":
            await state.set_state(BuyState.amount)
            await query.message.answer("Enter amount in ₹")

        elif callback_data.action == "prices":
            await query.message.answer(f"💰 Gold Price\n1g = ₹{GOLD_PRICE}")
