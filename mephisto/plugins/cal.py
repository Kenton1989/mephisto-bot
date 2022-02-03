import math
import logging

from nonebot import on_command, CommandSession

import math_expr as me

log = logging.getLogger('/cal')

MAX_PARAM_TXT_LEN = 50


@on_command('cal', aliases=('calculate', '算', '计算'), only_to_me=False)
async def cal(session: CommandSession):

    expr_str = session.current_arg_text.strip()

    arg_len = len(expr_str)

    if arg_len > MAX_PARAM_TXT_LEN:
        await session.send('太长不看', at_sender=True)
        return

    if arg_len == 0:
        await session.send('你算啥？', at_sender=True)
        return

    try:
        res = me.evaluate(expr_str)
    except:
        log.warning('unknown expression %s', expr_str)
        await session.send('我读的书少，这能算吗？', at_sender=True)
        return
    
    reply = '\n结果：' + str(res) 
    await session.send(reply, at_sender=True)





