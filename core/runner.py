import asyncio
import logging

from core import misc, load

log = logging.getLogger(__name__)


async def _run():
    while misc.startup_funcs:
        fn = misc.startup_funcs.pop(0)

        if asyncio.iscoroutinefunction(fn):
            await fn()
        elif asyncio.iscoroutine(fn):
            await fn
        elif callable(fn):
            await misc.loop.run_in_executor(None, fn)

    del misc.startup_funcs


def run():
    load.load_packages()
    log.info('loaded packages')

    misc.loop.run_until_complete(_run())
    log.info('ran startup functions')

    load.register_handlers()
    log.info('registered handler')

    misc.loop.run_forever()
