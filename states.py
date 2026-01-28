from aiogram.fsm.state import State, StatesGroup

class BuyState(StatesGroup):
    amount = State()
    txid = State()
    screenshot = State()
