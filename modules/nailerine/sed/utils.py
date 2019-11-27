import re
from collections import defaultdict, deque

last_msgs = defaultdict(lambda: deque(maxlen=10))


async def doit(message, match):
    fr = match.group(1)
    to = match.group(2)
    to = (to
          .replace('\\/', '/')
          .replace('\\0', '\\g<0>'))
    try:
        fl = match.group(3)
        if fl is None:
            fl = ''
        fl = fl[1:]
    except IndexError:
        fl = ''

    # Build Python regex flags
    count = 1
    flags = 0
    for f in fl.lower():
        if f == 'i':
            flags |= re.IGNORECASE
        elif f == 'm':
            flags |= re.MULTILINE
        elif f == 's':
            flags |= re.DOTALL
        elif f == 'g':
            count = 0
        elif f == 'x':
            flags |= re.VERBOSE
        else:
            await message.reply('unknown flag: {}'.format(f))
            return

    def substitute(m):
        if not m.raw_text:
            return None

        s, i = re.subn(fr, to, m.raw_text, count=count, flags=flags)
        if i > 0:
            return s

    try:
        substitution = None
        if message.is_reply:
            substitution = substitute(await message.get_reply_message())
        else:
            for msg in reversed(last_msgs[message.chat_id]):
                substitution = substitute(msg)
                if substitution is not None:
                    break

        if substitution is not None:
            await message.reply(substitution)

    except Exception as e:
        await message.reply('fuck me\n' + str(e))
