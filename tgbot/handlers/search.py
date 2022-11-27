from aiogram.types import Message, URLInputFile, InputMediaPhoto, CallbackQuery

import localization
from tgbot.keyboards import inline
from tgbot.keyboards.callback import Pharmacy, Item
from tgbot.services.api import get_pharmacy, get_pharmacy_item


async def start(message: Message):
    await message.answer(localization.START)


async def search(message: Message):
    loading = await message.reply(localization.SEARCHING)
    data = await get_pharmacy(pharmacy_id=1, query=message.text)

    if data['status'] == 'ok':
        title = data['offers'][0]['title'].split()[0]
        price = data['offers'][0]['price']
        for offer in data['offers']:
            price = offer['price'] if price > offer['price'] else price

        await loading.delete()
        await message.reply_photo(
            photo=URLInputFile(data['offers'][0]['image'], filename=title),
            caption=localization.INFO.format(title=title, price=price),
            reply_markup=inline.pharmacy(pharmacy_id=1, query=message.text, offers=data['offers'])
        )
    else:
        await loading.edit_text(localization.NOT_FOUND)


async def pharmacy(query: CallbackQuery, callback_data: Pharmacy):
    loading = await query.message.reply(localization.SEARCHING)
    data = await get_pharmacy(pharmacy_id=callback_data.id, query=callback_data.query)

    if data['status'] == 'ok':
        title = data['offers'][0]['title'].split()[0]
        price = data['offers'][0]['price']
        for offer in data['offers']:
            if type(offer['price']) == int:
                price = offer['price'] if price > offer['price'] else price

        await loading.delete()
        await query.message.edit_media(
            media=InputMediaPhoto(
                media=URLInputFile(data['offers'][0]['image'], filename=title),
                caption=localization.INFO.format(title=title, price=price)
            ),
            reply_markup=inline.pharmacy(pharmacy_id=callback_data.id, query=callback_data.query, offers=data['offers'])
        )
    else:
        await loading.delete()
        await query.message.edit_caption(
            localization.NOT_FOUND,
            reply_markup=inline.pharmacy(pharmacy_id=callback_data.id, query=callback_data.query, offers=[])
        )


async def monastirev_item(query: CallbackQuery, callback_data: Item):
    item = await get_pharmacy_item(callback_data.pharmacy_id, callback_data.id)
    if item['status'] == 'ok':
        item = item['item']
        caption = localization.MONASTIREV_ITEM.format(
            title=item['title'], price=item['price'], description=item['description'].capitalize()
        )
        for key, value in item['additions'].items():
            key = key.replace(':', '')
            caption += f'👉 <b>{key}:</b> <code>{value}</code>\n'
        await query.message.reply_photo(
            photo=URLInputFile(item['image'], filename=item['title']),
            caption=caption,
            reply_markup=inline.url(item['link'])
        )
    else:
        await query.message.reply(localization.NOT_FOUND)
    await query.answer()


async def close_item(query: CallbackQuery):
    await query.message.delete()
