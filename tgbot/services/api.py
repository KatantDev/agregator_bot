import logging
import aiohttp

from tgbot.config import load_config

config = load_config('.env')
logger = logging.getLogger(__name__)


async def get_pharmacy(pharmacy_id, query):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'{config.misc.base_url}/get_pharmacies/{pharmacy_id}',
                params={'query': query}
        ) as response:
            return await response.json()


async def get_pharmacy_item(pharmacy_id, item):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'{config.misc.base_url}/get_pharmacy_item/{pharmacy_id}',
                params={'item': item}
        ) as response:
            return await response.json()
