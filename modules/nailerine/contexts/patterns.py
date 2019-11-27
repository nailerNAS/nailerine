import re

join_leave = re.compile(r'(?i)\.as\s\w+\s(join|leave)\s')
send = re.compile(r'(?i)\.as\s\w+\s')
