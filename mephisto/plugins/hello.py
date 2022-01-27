from nonebot import on_command, CommandSession

from nonebot import default_config as cfg

@on_command('hello', aliases=('你好'))
async def hello(session: CommandSession):
    await session.send('你寄吧谁呀')
