import typing
from datetime import datetime

# noinspection PyProtectedMember
from aiojobs import Scheduler
from telethon import TelegramClient, events
from telethon.tl import custom

ClientList = typing.Dict[str, TelegramClient]
Handler = typing.Union[typing.Callable, typing.Awaitable]
HandlerList = typing.List[Handler]
Packages = typing.Iterable[str]
OmwChats = typing.Dict[int, Scheduler]
IntList = typing.List[int]
Sections = typing.List[str]
ClientDict = typing.Dict[int, TelegramClient]
DictList = typing.List[typing.Dict[str, str]]
StrOrNone = typing.Optional[str]
DateList = typing.List[datetime]
ChatDatesDict = typing.DefaultDict[int, DateList]
EventLike = typing.Union[events.NewMessage.Event, custom.Message]
StartupFuncs = typing.List[typing.Union[typing.Callable, typing.Awaitable, typing.Coroutine]]
FromToDict = typing.DefaultDict[int, typing.DefaultDict[str, typing.Optional[int]]]
IntTaskDict = typing.Dict[int, Scheduler]
