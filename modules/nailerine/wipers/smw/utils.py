from datetime import datetime, timedelta
from typing import List

import pytz

from core import misc
from modules.db_model.context import Context
from modules.db_model.smw import SmwChat
from modules.nailerine.wipers.smw.misc import task
from modules.utils import aiowrap

utc = pytz.utc
ukr = pytz.timezone('Europe/Kiev')
fmt = '%d-%m-%Y %H:%M'


def dt_input(dt: datetime) -> datetime:
    if not dt.tzinfo:
        dt: datetime = ukr.localize(dt)
    return dt.astimezone(utc)


def dt_output(dt: datetime) -> datetime:
    if not dt.tzinfo:
        dt: datetime = utc.localize(dt)
    return dt.astimezone(ukr)


def utc_time() -> datetime:
    dt = datetime.utcnow()
    dt: datetime = utc.localize(dt)

    return dt


def ukr_time() -> datetime:
    return utc_time().astimezone(ukr)


@aiowrap
def enable_chat(chat_id: int, client_name: str, hour: int, minute: int):
    dt = ukr_time()
    dt = dt.replace(hour=hour, minute=minute)
    dt = dt_input(dt)
    if utc_time() >= dt:
        dt += timedelta(days=1)

    with Context() as c:
        smw_chat: SmwChat = c.query(SmwChat).get(chat_id)
        if smw_chat:
            smw_chat.next_date = dt
        else:
            smw_chat = SmwChat(id=chat_id,
                               next_date=dt,
                               client_name=client_name)
            c.add(smw_chat)
    misc.loop.create_task(task.task())


@aiowrap
def disable_chat(chat_id: int):
    with Context() as c:
        smw_chat: SmwChat = c.query(SmwChat).get(chat_id)
        if smw_chat:
            c.delete(smw_chat)


@aiowrap
def get_chat(chat_id: int) -> SmwChat:
    with Context(False) as c:
        smw_chat = c.query(SmwChat).get(chat_id)
        c.expunge_all()

        return smw_chat


async def get_chats() -> List[SmwChat]:
    with Context(False) as c:
        smw_chats = c.query(SmwChat).all()
        c.expunge_all()

        return smw_chats


@aiowrap
def chats_available() -> bool:
    with Context(False) as c:
        smw_chat = c.query(SmwChat).first()
        c.expunge_all()

        return bool(smw_chat)


async def get_next_date(chat_id: int) -> datetime:
    smw_chat = await get_chat(chat_id)

    return dt_output(smw_chat.next_date)


async def get_delta(chat_id: int) -> timedelta:
    smw_chat = await get_chat(chat_id)

    return smw_chat.next_date - datetime.utcnow()
