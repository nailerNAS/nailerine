import io
import logging
import os
from asyncio import get_event_loop, iscoroutine, iscoroutinefunction
from contextlib import suppress
from random import choice

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon import TelegramClient

from config import commandos, nailerine_bot_token
from core import hints
from modules.anti_flood.controller import Controller
from modules.nailerine_bot.login.config_worker import ConfigWorker
from .load import load_packages

log = logging.getLogger(__name__)

loop = get_event_loop()
clients: hints.ClientList = {}
handlers: hints.HandlerList = []
client_ids: hints.IntList = []
controller = Controller()
bot = Bot(nailerine_bot_token, loop)
dp = Dispatcher(bot, loop, MemoryStorage())
startup_funcs: hints.StartupFuncs = []
gc_protected = []

for session in ConfigWorker.get_sections():
    api_id = ConfigWorker.get_api_id(session)
    api_hash = ConfigWorker.get_api_hash(session)

    if all((api_id, api_hash)):
        clients[session] = TelegramClient(f'sessions/{session}', api_id, api_hash)


async def _check_accounts() -> str:
    with io.StringIO() as string:
        string.write('Launching Nailerine\n\n')
        for name, client in clients.items():
            await client.connect()
            if await client.is_user_authorized():
                log.info('%s connected', name)
                string.write(f'{name} connected\n')
            else:
                log.warning('%s is broken, removing', name)
                string.write(f'{name} is broken, removing\n')
                ConfigWorker.del_section(name)
                with suppress(Exception):
                    os.remove(f'./sessions/{name}.session')
                with suppress(Exception):
                    os.remove(f'./sessions/{name}.session-journal')

        return string.getvalue()


async def _run_startup_funcs():
    while startup_funcs:
        fn = startup_funcs.pop(0)

        if iscoroutinefunction(fn):
            await fn()
        elif iscoroutine(fn):
            await fn
        elif callable(fn):
            await loop.run_in_executor(None, fn)


def _register_handlers():
    for client in clients.values():
        for handler in handlers:
            client.add_event_handler(handler)
    handlers.clear()


async def _start():
    check_result = await _check_accounts()
    await (await choice(list(clients.values())).send_message(commandos, check_result)).pin(notify=True)
    log.info('accounts checked')

    load_packages()
    log.info('packages loaded')

    await _run_startup_funcs()
    log.info('ran startup functions')

    _register_handlers()
    log.info('registered handlers')

    log.info('starting polling')

    await dp.skip_updates()
    try:
        await dp.start_polling(reset_webhook=True)
    except KeyboardInterrupt:
        log.warning('stopping polling')
        dp.stop_polling()

    log.warning('disconnecting clients')
    for client in clients.values():
        await client.disconnect()


def start():
    loop.run_until_complete(_start())
