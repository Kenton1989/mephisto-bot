import os
import logging
import math
import time
from random import randint

from nonebot import on_command, CommandSession

l = logging.Logger('/hello')

@on_command('dice', aliases=('色子', '骰子'), shell_like=True)
async def hello(session: CommandSession):

    arg_cnt = len(session.argv)
    if arg_cnt == 0:
        await session.send("骰子呢？", at_sender=True)
        return
    
    if arg_cnt > 1:
        await session.send("骰子多了不起啊？", at_sender=True)
        return

    mx_str = session.argv[0]

    if len(mx_str) > 12:
        await session.send("整这阴间数据有意思🐎？", at_sender=True)
        return

    try:
        mx = float(mx_str)
    except:
        try:
            mx = int(mx_str, base=0)
            await session.send("你以为我只认得十进制啊？", at_sender=True)
            time.sleep(1)
        except:
            await session.send("识不识数啊你？", at_sender=True)
            return

    if mx < 0:
        await session.send("这是什么反物质骰子？", at_sender=True)
        return

    mx_int = math.floor(mx)
    if mx_int != mx:
        fraction = mx - mx_int
        if fraction >= 0.01:
            rep = "你家骰子能有%.2f个面？" % fraction
        else:
            rep = "你家骰子能有%.2e个面？" % fraction
        await session.send(rep, at_sender=True)
        return

    if mx_int <= 0:
        await session.send("丢空气是吧？", at_sender=True)
        return

    if mx_int <= 1:
        await session.send("这骰子有啥好丢的？", at_sender=True)
        return

    upper_bound = randint(100000000, 200000000)
    if mx_int > upper_bound:
        await session.send("骰子好大，丢不动，爬！", at_sender=True)
        return

    await session.send("丢完了，%d点" % randint(1, mx_int))

    

