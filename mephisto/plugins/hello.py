import os
import logging

from nonebot import on_command, CommandSession

import env

l = logging.Logger('/hello')

@on_command('hello', aliases=('你好'))
async def hello(session: CommandSession):
    if session.event.user_id in env.SUPERUSER:
        await session.send('你好')
    else:
        await session.send('你寄吧谁啊')
