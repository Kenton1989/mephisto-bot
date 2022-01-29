import math
import logging

from nonebot import on_command, CommandSession

import env

l = logging.Logger('/cal')

MAX_PARAM_TXT_LEN = 40


@on_command('cal', aliases=('eval', '算', '计算'), shell_like=True, only_to_me=False)
async def cal(session: CommandSession):

    if len(session.current_arg_text) > MAX_PARAM_TXT_LEN:
        await session.send('太长不看', at_sender=True)
        return

    if arg_cnt < 0:
        await session.send('你算啥？', at_sender=True)
        return 

    reply = ''

    if arg_cnt > 1:
        reply += '\n我只算第一个式子'

    expr_str = session.argv[0]

    try:
        res = me.evaluate(expr_str)
        if math.isnan(res):
            raise Exception()
    except:
        await session.send('我读的书少，这能算吗？', at_sender=True)
        return
    
    reply += '\n结果：' + str(res) 
    await session.send(reply, at_sender=True)





