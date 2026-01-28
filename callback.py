from aiogram.filters.callback_data import CallbackData

class MainCB(CallbackData, prefix="main"):
    action: str

class ConfirmBuyCB(CallbackData, prefix="confirm"):
    pid: int
