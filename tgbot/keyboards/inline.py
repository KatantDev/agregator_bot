import typing

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import localization
from tgbot.keyboards.callback import Pharmacy, Item


def url(link: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text='📎 Купить', url=link))
    keyboard.row(InlineKeyboardButton(text='✖️ Закрыть', callback_data='item:close'))
    return keyboard.as_markup()


def pharmacy(pharmacy_id: int, query: str, offers: typing.List[typing.Dict]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for offer in offers[:10]:
        if 'variant' not in offer or not offer["variant"]:
            text = f'{offer["title"]}'
        else:
            text = f'{offer["title"]} ({offer["variant"]})'
        if pharmacy_id == 1:
            item_id = offer['link'].split('/', maxsplit=5)[-1]
            keyboard.row(InlineKeyboardButton(
                text=text, callback_data=Item(pharmacy_id=pharmacy_id, id=item_id).pack()
            ))
        else:
            keyboard.row(InlineKeyboardButton(text=text, url=offer['link']))

    previous_pharmacy = InlineKeyboardButton(
        text=localization.PREV_PHARMACY,
        callback_data=Pharmacy(id=pharmacy_id - 1, query=query).pack()
    )
    next_pharmacy = InlineKeyboardButton(
        text=localization.NEXT_PHARMACY,
        callback_data=Pharmacy(id=pharmacy_id + 1, query=query).pack()
    )

    if pharmacy_id > 1:
        keyboard.row(previous_pharmacy)
        if pharmacy_id < 6:
            keyboard.add(next_pharmacy)
    elif pharmacy_id == 1:
        keyboard.row(next_pharmacy)
    return keyboard.as_markup()
