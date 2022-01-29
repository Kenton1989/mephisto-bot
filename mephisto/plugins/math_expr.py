import re
import math

import numexpr as ne

MATH_CONST = {'pi': math.pi, 'π': math.pi, 'e': math.e, 'inf': math.inf}

SUB_MAP = {
    # replace UTF char with ASCII char
    '（': '(',
    '）': ')',
    '，': ',',
    '÷': '/',
    '×': '*',
    '＋': '+',

    # replace common synonym
    'ln': 'log',
    '∞': 'inf',
    'mod': '%',
}

SUB_RE = re.compile('|'.join(re.escape(s) for s in SUB_MAP.keys()))

def evaluate(txt: str):
    txt = SUB_RE.sub(lambda m: SUB_MAP[m.group(0)], txt)
    return ne.evaluate(txt, local_dict=MATH_CONST).item()
