from aiohttp import ClientSession

DOGBIN = 'https://del.dog/'
DOGBIN_POST = 'https://del.dog/documents'

CONTENT = 'content'
SLUG = 'slug'
KEY = 'key'


async def paste(text: str) -> str:
    async with ClientSession() as session:
        data = {CONTENT: text,
                SLUG: ''}
        async with session.post(DOGBIN_POST, json=data) as resp:
            json = await resp.json()

            return f'{DOGBIN}{json[KEY]}'
