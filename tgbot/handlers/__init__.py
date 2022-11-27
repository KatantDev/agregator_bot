from aiogram import Router, F
from aiogram.filters import Command

from tgbot.handlers.search import start, search, pharmacy, monastirev_item, close_item
from tgbot.keyboards.callback import Pharmacy, Item

router = Router()

router.message.register(start, Command(commands=['start']))
router.message.register(search)
router.callback_query.register(pharmacy, Pharmacy.filter())
router.callback_query.register(monastirev_item, Item.filter(F.pharmacy_id == 1))
router.callback_query.register(close_item, F.data == 'item:close')
