import logging
import os
from logging import Formatter
from logging.handlers import RotatingFileHandler

from core import misc


def setup_logging():
    if not os.path.exists('./sessions/logs/'):
        os.mkdir('./sessions/logs/')

    fmt = '[%(levelname)s - %(asctime)s] %(name)s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)

    formatter = Formatter(fmt)
    handler = RotatingFileHandler('./sessions/logs/nailerine.log', maxBytes=1024 * 1024, backupCount=10)
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)

    logging.getLogger().addHandler(handler)


def main():
    setup_logging()
    misc.start()


if __name__ == '__main__':
    main()
