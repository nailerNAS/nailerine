import sys

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from core import hints
from core import misc
from core.misc import client_ids
from modules.nailerine_bot.login.config_worker import ConfigWorker
from modules.nailerine_bot.login import states

clients: hints.ClientDict = {}


@misc.dp.message_handler(commands=['login'])
async def login_command(message: Message):
    if message.from_user.id not in client_ids:
        await message.reply('You are not authorized to Nailerine though you can\'t authorize a new account')
    else:
        await states.Login.session.set()
        await message.reply('How to name a new session?')


@misc.dp.message_handler(state='*', commands=['cancel'])
async def cancel(message: Message, state: FSMContext, raw_state: str = None):
    if raw_state is None:
        return

    await state.finish()
    await message.reply('Canceled')


@misc.dp.message_handler(state=states.Login.session)
async def add_session(message: Message, state: FSMContext):
    session = message.text
    if session in ConfigWorker.get_sections():
        await message.reply('Session with this name already exists')
    else:
        ConfigWorker.add_section(session)
        async with state.proxy() as d:
            d['session'] = session

        await states.Login.next()
        await message.reply('Done! Now send me API ID')


@misc.dp.message_handler(state=states.Login.api_id)
async def set_api_id(message: Message, state: FSMContext):
    async with state.proxy() as d:
        session = d['session']
        ConfigWorker.set_api_id(session, message.text)

    await states.Login.next()
    await message.reply('Now send me API Hash')


@misc.dp.message_handler(state=states.Login.api_hash)
async def set_api_hash(message: Message, state: FSMContext):
    async with state.proxy() as d:
        session = d['session']
        ConfigWorker.set_api_hash(session, message.text)

    await states.Login.next()
    await message.reply('Now send me phone number')


@misc.dp.message_handler(state=states.Login.number)
async def send_phone(message: Message, state: FSMContext):
    session = None

    async with state.proxy() as d:
        session = d['session']

    api_id = ConfigWorker.get_api_id(session)
    api_hash = ConfigWorker.get_api_hash(session)

    async with state.proxy() as d:
        cli = TelegramClient(f'sessions/{session}', api_id, api_hash)
        clients[message.chat.id] = cli

        await cli.connect()
        if not await cli.is_user_authorized():
            try:
                d['number'] = message.text
                await cli.send_code_request(phone=message.text)
                await states.Login.next()
                await message.reply('Now send me the code (put a space somewhere in the middle)')
            except Exception as e:
                await message.reply(f'{e}')


@misc.dp.message_handler(state=states.Login.code)
async def send_code(message: Message, state: FSMContext):
    async with state.proxy() as d:
        cli = clients[message.chat.id]
        try:
            await cli.sign_in(phone=d['number'], code=message.text.replace(' ', ''))
            await message.reply('Nailerine has connected to this account and is being restarted. . .')
            sys.exit(-1)

        except SessionPasswordNeededError:
            await states.Login.next()
            await message.reply('Now send me 2FA password')

        except Exception as e:
            await message.reply(f'{e}')


@misc.dp.message_handler(state=states.Login.password)
async def send_password(message: Message, state: FSMContext):
    cli = clients[message.chat.id]
    try:
        await cli.sign_in(password=message.text)
        await message.reply('Nailerine has connected to this account and is being restarted. . .')

        import sys
        sys.exit(1)

    except Exception as e:
        await message.reply(f'{e}')
