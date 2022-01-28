import logging
import re
import random

import aiocqhttp

import nonebot
from nonebot import NoneBot
from nonebot.plugin import PluginManager
from nonebot.message import CanceledException

log = logging.Logger('random_echo')

echo_prob = 0.02

last_sent = None

@nonebot.message_preprocessor
async def random_echo(bot: NoneBot, event: aiocqhttp.Event, plugin_manager: PluginManager):
    if random.random() > echo_prob:
        return

    # check event type
    if event.type != "message" or event.detail_type != "group":
        return
    msg = event.message

    # avoid infinit echo
    global last_sent
    if msg == last_sent:
        return

    # check if msg maybe a command
    msg_str: str = msg.extract_plain_text()
    for cmd_prefix in bot.config.COMMAND_START:
        if re.match(cmd_prefix, msg_str):
            return

    nonebot.logger.info("triggered random_echo @[group: %d]", event.group_id)
    last_sent = msg

    await bot.send(event, msg)

    raise CanceledException("random echo handled")
