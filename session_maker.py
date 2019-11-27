import os
from configparser import ConfigParser
from os import path

from telethon.sync import TelegramClient

import config


def main():
    if not path.isfile(config.sessions):
        os.makedirs(path.dirname(config.sessions), exist_ok=True)
        open(config.sessions, 'w').close()

    cfg = ConfigParser()
    cfg.read(config.sessions)

    session = input('Session: ')
    assert session not in cfg.sections()
    cfg.add_section(session)

    api_id = input('API ID: ')
    cfg[session]['api_id'] = api_id

    api_hash = input('API Hash: ')
    cfg[session]['api_hash'] = api_hash

    with open(config.sessions, 'wt') as file:
        cfg.write(file)

    client = TelegramClient(f'./sessions/{session}', api_id, api_hash)
    client.start()
    client.disconnect()


if __name__ == '__main__':
    main()
