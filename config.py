from os import getenv
from typing import Type


def get(key: str, default=None, converter: Type = None):
    val = getenv(key, default)
    return converter(val) if converter else val


sessions = './sessions/sessions.ini'
zero = '͏'
conn_string = 'sqlite:///./sessions/sqlite3.db'

commandos = get('commandos')
commandos_id = get('commandos_id', converter=int)
nailerine_bot_token = get('nailerine_bot_token')
mini_nailerine = get('mini_nailerine')
