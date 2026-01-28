from datetime import datetime
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from states import BuyState
from callbacks import ConfirmBuyCB
from config import GOLD_PRICE, OWNER_ID, UPI_ID, PAYEE_NAME
from database import cur, conn

def register(dp, bot):

    @dp.message(BuyState.amount)
    async def buy_amount(message: types.Message, state: FSMContext):
        amount = float(message.text)
        gold = amount / GOLD_PRICE
        await state.update_data(amount=amount, gold=gold)
        await state.set_state(BuyState.txid)
        await message.answer(
            f"Send ₹{amount} to <code>{UPI_ID}</code>\nPayee: {PAYEE_NAME}"
        )

    @dp.message(BuyState.txid)
    async def buy_txid(message: types.Message, state: FSMContext):
        await state.update_data(txid=message.text)
        await state.set_state(BuyState.screenshot)
        await message.answer("Send screenshot")

    @dp.message(BuyState.screenshot)
    async def buy_screenshot(message: types.Message, state: FSMContext):
        data = await state.get_data()
        file_id = message.photo[-1].file_id
        cur.execute(
            "INSERT INTO purchases (user_id, amount, gold, txid, screenshot, time) VALUES (?, ?, ?, ?, ?, ?)",
            (message.from_user.id, data["amount"], data["gold"], data["txid"], file_id, datetime.now().isoformat())
        )
        conn.commit()

        pid = cur.lastrowid
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Confirm", callback_data=ConfirmBuyCB(pid=pid).pack())]
        ])
        await bot.send_message(OWNER_ID, "New buy request", reply_markup=kb)
        await bot.send_photo(OWNER_ID, file_id)
        await message.answer("⏳ Sent for verification")
        await state.clear()

    @dp.callback_query(ConfirmBuyCB.filter())
    async def confirm_buy(query: CallbackQuery, callback_data: ConfirmBuyCB):
        if query.from_user.id != OWNER_ID:
            return
        row = cur.execute("SELECT user_id, gold FROM purchases WHERE id=?", (callback_data.pid,)).fetchone()
        cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (row[0],))
        cur.execute("UPDATE users SET gold = gold + ? WHERE user_id=?", (row[1], row[0]))
        cur.execute("UPDATE purchases SET confirmed=1 WHERE id=?", (callback_data.pid,))
        conn.commit()
        await bot.send_message(row[0], f"✅ {row[1]:.4f} g gold added")
