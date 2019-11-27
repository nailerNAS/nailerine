import json
import logging
from io import StringIO

from telethon import events

from core import misc, hints
from modules.nailerine.contexts import patterns, utils

log = logging.getLogger(__name__)

vars_dict = {}


@events.register(events.NewMessage(outgoing=True, pattern=patterns.join_leave))
async def join_as(event: hints.EventLike):
    text_split: list = event.text.split()
    client_name = text_split[1]
    option = text_split[2]
    link = text_split[3]

    link = vars_dict[link] if link in vars_dict else link

    client = misc.clients[client_name]
    if option == 'join':
        log.info('joining %s as %s', client_name, link)
        await utils.join(client, link)
    else:
        log.info('leaving %s as %s', client_name, link)
        await utils.leave(client, link)


@events.register(events.NewMessage(outgoing=True, pattern=patterns.send))
async def send_as(event: hints.EventLike):
    text_split: list = event.text.split(maxsplit=4)
    client_name = text_split[1]
    link = text_split[3]
    text = text_split[4]

    link = event.chat_id if link == 'here' else vars_dict[link] if link in vars_dict else link

    client = misc.clients[client_name]
    log.info('sending %s as %s to %s', text, client_name, text)
    await utils.send(client, link, text)


@events.register(events.NewMessage(outgoing=True, pattern=r'\.set (?P<key>\w+) (?P<val>.+)'))
async def ctx_set(event: hints.EventLike):
    key = event.pattern_match.group('key')
    val = event.pattern_match.group('val')

    vars_dict[key] = val

    await event.edit(f'```{key} is now set to {val}```')


@events.register(events.NewMessage(outgoing=True, pattern=r'\.unset (?P<key>\w+)'))
async def ctx_unset(event: hints.EventLike):
    key = event.pattern_match.group('key')
    if key == 'all':
        vars_dict.clear()
        await event.edit('```All vars were forgotten```')
    else:
        if key in vars_dict:
            val = vars_dict.pop(key)
            await event.edit(f'```{key} ({val}) was forgotten```')
        else:
            await event.edit('```It was not even set```')


@events.register(events.NewMessage(outgoing=True, pattern=r'\.vars'))
async def ctx_list(event: hints.EventLike):
    text = '```No vars are set```'
    if vars_dict:
        with StringIO() as string:
            string.write('```')
            string.write(json.dumps(list(vars_dict.keys()), indent=2))
            string.write('```')

            text = string.getvalue()

    await event.edit(text)


misc.handlers.extend((join_as,
                      send_as,
                      ctx_set,
                      ctx_unset,
                      ctx_list))
