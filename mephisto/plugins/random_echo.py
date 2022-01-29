import logging
import re
import random

import aiocqhttp

import nonebot
from nonebot import NoneBot
from nonebot.plugin import PluginManager
from nonebot.message import CanceledException

log = logging.Logger('random_echo')

ECHO_PROB = 0.01

last_sent = None

CAN_ECHO_TYPE = {'text', 'face'}

@nonebot.message_preprocessor
async def random_echo(bot: NoneBot, event: aiocqhttp.Event, plugin_manager: PluginManager):
    if random.random() > ECHO_PROB:
        return

    # check event type
    if event.type != "message" or event.detail_type != "group":
        return

    msg: aiocqhttp.Message = event.message

    # avoid infinit echo
    global last_sent
    if msg == last_sent:
        return

    # check if msg maybe a command
    msg_str: str = msg.extract_plain_text()
    for cmd_prefix in bot.config.COMMAND_START:
        if re.match(cmd_prefix, msg_str):
            return

    # check can easily echo or not
    if any(m.type not in CAN_ECHO_TYPE for m in msg):
        return

    nonebot.logger.info("triggered random_echo @[group: %d]", event.group_id)
    last_sent = msg

    await bot.send(event, msg)

    raise CanceledException("random echo handled")
