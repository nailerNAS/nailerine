from contextlib import redirect_stdout
from io import StringIO
from subprocess import PIPE, Popen
from traceback import format_exc
from typing import Callable

from modules.utils import aiowrap


def wrap_code(code: str) -> str:
    with StringIO() as string:
        string.write('async def __ex(event=None, client=None):\n')
        for line in code.splitlines(True):
            string.write(f'\t{line}')

        return string.getvalue()


def get_callable(code: str) -> Callable:
    exec(wrap_code(code))
    return locals()['__ex']


async def execute(code: str, event=None, client=None):
    with StringIO() as stdout:
        with redirect_stdout(stdout):
            try:
                fn = get_callable(code)
                await fn(event, client)
            except:
                print(format_exc())

        return stdout.getvalue()


@aiowrap
def bash(code: str) -> str:
    proc = Popen(code,
                 executable='/bin/bash',
                 stdout=PIPE,
                 stderr=PIPE,
                 shell=True,
                 universal_newlines=True)
    result = proc.stdout.read() + proc.stderr.read()

    return result
