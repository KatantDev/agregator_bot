from aiogram.filters.callback_data import CallbackData


class Pharmacy(CallbackData, prefix="pharmacy"):
    id: int
    query: str


class Item(CallbackData, prefix="item"):
    pharmacy_id: int
    id: str
