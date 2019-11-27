import io
import os
from os import listdir, remove
from zipfile import ZipFile

from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InputFile

import config
from core import misc
from core.misc import client_ids
from modules.nailerine_bot.login.config_worker import ConfigWorker


@misc.dp.message_handler(commands=['ping'])
async def ping(message: Message):
    text = 'Pong!\n'

    if message.from_user.id in client_ids:
        text += 'Your account is authorized in Nailerine\nUse the /login command to authorize a new account'
    else:
        text += 'Your account is not authorized in Nailerine'

    await message.reply(text)


@misc.dp.message_handler(lambda m: m.from_user.id in client_ids, commands=['del'])
async def del_account(message: Message):
    words = message.text.split()
    if len(words) >= 2:
        section = words[1]
        ConfigWorker.del_section(section)

        if f'{section}.session' in listdir('./sessions/'):
            remove(f'./sessions/{section}.session')
        if f'{section}.session-journal' in listdir('./sessions/'):
            remove(f'./sessions/{section}.session-journal')

        await message.reply(f'Section {section} has been deleted')


@misc.dp.inline_handler(lambda q: q.query == 'Hello from big Nailerine')
async def inline_ping(query: InlineQuery):
    if query.from_user.id in client_ids:
        content = InputTextMessageContent('mini Nailerine has started')
        result = InlineQueryResultArticle(id='1',
                                          title='f',
                                          input_message_content=content,
                                          description='f')
        await query.answer([result], cache_time=1, is_personal=True)


@misc.dp.message_handler(lambda m: m.from_user.id in client_ids, commands=['logs'])
async def send_logs(message: Message):
    logs_dir = './sessions/logs/'

    with io.BytesIO() as file:
        with ZipFile(file, 'w') as zip_file:
            for log_file in os.listdir(logs_dir):
                zip_file.write(f'{logs_dir}{log_file}')
        file.seek(0)
        await message.reply_document(InputFile(file, 'logs.zip'))


@misc.dp.message_handler(commands=['ids'])
@misc.dp.channel_post_handler(lambda m: m.text and m.text == '/ids')
async def check_ids(message: Message):
    with io.StringIO() as text:
        text.write(f'ID from event: {message.chat.id}\n')
        text.write(f'ID from config: {config.commandos_id}\n')
        text.write(f'Equality: {message.chat.id == config.commandos_id}')

        await message.reply(text.getvalue())
