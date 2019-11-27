from configparser import ConfigParser
from enum import Enum, auto

from config import sessions
from core import hints


class Options(Enum):
    api_id = auto()
    api_hash = auto()


class ConfigWorker:
    __slots__ = ['config']

    def __enter__(self):
        self.config = ConfigParser()
        self.config.read(sessions)
        return self.config

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(sessions, 'w') as f:
            self.config.write(f)

    @classmethod
    def get_sections(cls) -> hints.Sections:
        with cls() as cfg:
            return cfg.sections()

    @classmethod
    def add_section(cls, section: str):
        with cls() as cfg:
            cfg.add_section(section)
            cfg[section][Options.api_id.name] = ''
            cfg[section][Options.api_hash.name] = ''

    @classmethod
    def del_section(cls, section: str):
        with cls() as cfg:
            cfg.remove_section(section)

    @classmethod
    def get_api_id(cls, section: str) -> int:
        with cls() as cfg:
            return cfg.getint(section, Options.api_id.name)

    @classmethod
    def set_api_id(cls, section: str, api_id: int):
        with cls() as cfg:
            cfg.set(section, Options.api_id.name, api_id)

    @classmethod
    def get_api_hash(cls, section: str) -> str:
        with cls() as cfg:
            return cfg.get(section, Options.api_hash.name)

    @classmethod
    def set_api_hash(cls, section: str, api_hash: str):
        with cls() as cfg:
            return cfg.set(section, Options.api_hash.name, api_hash)
