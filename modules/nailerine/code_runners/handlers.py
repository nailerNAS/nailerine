import io
from asyncio import gather
from html import escape

from telethon.events import NewMessage, register

from core import hints
from core.misc import handlers
from .runner import bash, execute


def format_run(code: str, output: str, executor: str = 'Exec'):
    code = escape(code)
    output = escape(output)

    return f'<b>{executor}:</b>\n' \
           f'<code>{code}</code>\n\n' \
           f'<b>Output:</b>\n' \
           f'<code>{output}</code>'


@register(NewMessage(outgoing=True, pattern=r'(\.ex\s).+'))
async def run_exec(event: hints.EventLike):
    cmd = event.pattern_match.group(1)
    code: str = event.raw_text
    code = code.replace(cmd, '', 1)

    output = await execute(code, event, event.client)
    output = format_run(code, output)

    if len(output) > 4096:
        with io.BytesIO() as file:
            file.name = 'exec.html'
            file.write(output.encode())
            file.seek(0)

            await gather(event.delete(),
                         event.respond(file=file))
    else:
        await event.edit(output, parse_mode='html')


@register(NewMessage(outgoing=True, pattern=r'(\.bash\s).+'))
async def run_bash(event: hints.EventLike):
    code = event.raw_text.replace(event.pattern_match.group(1), '')
    output = await bash(code)
    output = format_run(code, output, 'Bash')

    if len(output) > 4096:
        with io.BytesIO() as file:
            file.name = 'bash.htm'
            file.write(output)
            file.seek(0)
            await event.reply(file=file)
    else:
        await event.edit(output, parse_mode='html')


handlers.extend(
    (
        run_exec,
        run_bash,
    )
)
