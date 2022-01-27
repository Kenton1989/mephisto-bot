from nonebot import on_command, CommandSession

from nonebot import default_config as cfg

@on_command('hello')
async def hello(session: CommandSession):
    print("/hello", session.current_arg_text.strip())
    await session.send('You TM who?')
