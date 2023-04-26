import re
from functools import reduce

PATTERNS = [
    lambda x: re.sub(r'”', r'"', x),
    lambda x: re.sub(r'’', r"'", x),
    lambda x: re.sub(r'([A-Za-z])-[\s\n]+([A-Za-z])', r'\1\2', x)
]

def fix_text(text):
    return reduce(lambda a, b: b(a), PATTERNS, text)