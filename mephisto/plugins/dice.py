import os
import logging
import math
from random import randint

from nonebot import on_command, CommandSession

l = logging.Logger('/hello')

@on_command('dice', aliases=('色子', '骰子'))
async def hello(session: CommandSession):

    arg_cnt = len(session.argv)
    if arg_cnt == 0:
        await session.send("骰子呢？", at_sender=True)
        return
    
    if arg_cnt > 1:
        await session.send("骰子多了不起啊？", at_sender=True)
        return

    mx_str = session.argv[0]
    try:
        mx = float(mx_str)
    except:
        await session.send("识不识数啊你？", at_sender=True)
        return

    if mx < 0:
        await session.send("这是什么反物质骰子？", at_sender=True)
        return

    mx_int = math.floor(mx)
    if mx_int != mx:
        rep = "你家骰子能有%2e个面？" % (mx - mx_int)
        await session.send(rep, at_sender=True)
        return

    if mx_int <= 1:
        await session.send("这骰子有啥好丢的？", at_sender=True)
        return

    upper_bound = randint(100000000, 200000000)
    if mx_int > upper_bound:
        await session.send("骰子好大，丢不动，爬！", at_sender=True)
        return

    await session.send("丢完了，%d点", randint(1, mx_int))

    

