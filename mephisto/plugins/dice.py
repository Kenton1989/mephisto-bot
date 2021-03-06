import os
import logging
import math
import time
from random import randint

from nonebot import on_command, CommandSession

import math_expr as me

log = logging.getLogger('/dice')

MAX_PARAM_TXT_LEN = 12

EPS = 1e-14

@on_command('dice', aliases=('色子', '骰子'), shell_like=True, only_to_me=False)
async def dice(session: CommandSession):

    arg_cnt = len(session.argv)
    if arg_cnt == 0:
        await session.send('骰子呢？', at_sender=True)
        return

    if arg_cnt > 1:
        await session.send('骰子多了不起啊？', at_sender=True)
        return

    mx_str = session.argv[0]

    if len(session.current_arg_text) > MAX_PARAM_TXT_LEN:
        await session.send('太长不看', at_sender=True)
        return

    try:
        mx = me.evaluate(mx_str)
    except:
        await session.send('我读的书少，这事数吗？', at_sender=True)
        return

    if not isinstance(mx, (int, float)) or math.isnan(mx):
        await session.send('你知道什么是自然数吗？', at_sender=True)
        return

    if mx < 0:
        await session.send('这是什么反物质骰子？', at_sender=True)
        return

    upper_bound = randint(100000000, 200000000)
    if mx > upper_bound:
        await session.send('骰子好大，丢不动，爬！', at_sender=True)
        return

    mx_int = int(mx)
    fraction = mx - mx_int
    if fraction > EPS:
        if fraction >= 0.01:
            rep = '你家骰子能有%.2f个面？' % fraction
        else:
            rep = '你家骰子能有%.2e个面？' % fraction
        await session.send(rep, at_sender=True)
        return

    if mx_int <= 0:
        await session.send('丢空气是吧？', at_sender=True)
        return

    if mx_int <= 1:
        await session.send('这骰子有啥好丢的？', at_sender=True)
        return


    await session.send('丢完了，%d点' % randint(1, mx_int), at_sender=True)
