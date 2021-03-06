import logging
import re
import random
import datetime
import os
import json
import atexit
import threading
from typing import Dict, Tuple

import aiocqhttp

import nonebot
from nonebot import NoneBot, CommandSession, on_command
from nonebot.plugin import PluginManager
from nonebot.message import CanceledException

from random_echo.config import *

log = logging.getLogger('random_echo')

last_sent = None

CAN_ECHO_TYPE = {'text', 'face'}


class Stat:
    def __init__(self, data: dict = {}):
        timestamp = data.get(
            'start-time', datetime.datetime.utcnow().timestamp())
        self.start_time = datetime.datetime.utcfromtimestamp(timestamp)
        self.total_msg = data.get('total-msg', 0)
        self.total_rep = data.get('total-rep', 0)

    @property
    def rep_ratio(self):
        return self.total_rep / self.total_msg

    def to_dict(self):
        return {
            'start-time': self.start_time.timestamp(),
            'total-msg': self.total_msg,
            'total-rep': self.total_rep,
        }


group_stats: Dict[int, Stat] = {}
group_sender_stats: Dict[int, Dict[int, Stat]] = {}


def load_stat(filename='random_echo.stat.json'):
    if not os.path.exists(filename):
        return

    with open(filename, 'r') as file:
        data = json.load(file)

    global group_stats, group_sender_stats

    group_stats = dict((int(k), Stat(v))
                       for k, v in data.get('group_stats', {}).items())

    group_sender_stats_raw = data.get('group_sender_stats', {})
    for k, v in group_sender_stats_raw.items():
        v = dict((int(k0), Stat(v0)) for k0, v0 in v.items())
        group_sender_stats[int(k)] = v


def save_stat(filename='random_echo.stat.json'):
    global group_stats, group_sender_stats
    data = {}
    data['group_stats'] = dict((str(k), v.to_dict())
                               for k, v in group_stats.items())
    data['group_sender_stats'] = {}
    for k, v in group_sender_stats.items():
        v = dict((str(k0), v0.to_dict()) for k0, v0 in v.items())
        data['group_sender_stats'][str(k)] = v

    with open(filename, 'w') as file:
        json.dump(data, file)


load_stat()
# auto save on exit
atexit.register(save_stat)
# auto save every 1 minute
threading.Timer(60, save_stat)

@nonebot.message_preprocessor
async def random_echo(bot: NoneBot, event: aiocqhttp.Event, plugin_manager: PluginManager):
    # check event type
    if event.type != "message" or event.detail_type != "group":
        return

    if event.self_id == event.user_id:
        return

    msg: aiocqhttp.Message = event.message

    global group_stats, group_sender_stats
    group_stat = group_stats.setdefault(event.group_id, Stat())
    sender_stats = group_sender_stats.setdefault(event.group_id, {})
    sender_stat = sender_stats.setdefault(event.user_id, Stat())

    group_stat.total_msg += 1
    sender_stat.total_msg += 1

    global ECHO_PROB, DEFAULT_ECHO_PROB
    echo_prob = ECHO_PROB.get(event.group_id, DEFAULT_ECHO_PROB)
    if random.random() > echo_prob:
        return

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

    group_stat.total_rep += 1
    sender_stat.total_rep += 1

    log.info("triggered random_echo @[group: %d]", event.group_id)
    last_sent = msg

    await bot.send(event, msg)

    raise CanceledException("random echo handled")


@on_command('random-echo-stat', aliases=('????????????', '????????????', '????????????'), permission=nonebot.permission.SUPERUSER)
async def echo_stat(session: CommandSession):
    event = session.event
    grp_id = event.group_id
    try:
        grp_id = int(session.current_arg_text)
    except:
        pass

    global group_stats, group_sender_stats
    group_stat = group_stats.get(grp_id, None)
    sender_stats = group_sender_stats.get(grp_id, None)

    if group_stat is None or sender_stats is None:
        session.finish('????????????????????????', at_sender=True)

    msg = ''

    if grp_id != event.group_id:
        msg += f'\n??????????????????{grp_id}'

    msg += f'\n??????{group_stat.start_time}??????????????????{group_stat.total_msg}?????????????????????{group_stat.total_rep}???????????????????????????{group_stat.rep_ratio}???'

    if group_stat.total_rep > 0:
        one_item = next(iter(sender_stats.items()))

        most_msg = one_item
        most_rep = one_item
        top_rep_ratio = one_item

        for res in sender_stats.items():
            stat = res[1]
            if stat.total_msg > most_msg[1].total_msg:
                most_msg = res
            if stat.total_rep > most_rep[1].total_rep:
                most_rep = res
            if stat.rep_ratio > top_rep_ratio[1].rep_ratio:
                top_rep_ratio = res

        most_msg_user = await session.bot.get_group_member_info(group_id=grp_id, user_id=most_msg[0])
        most_rep_user = await session.bot.get_group_member_info(group_id=grp_id, user_id=most_rep[0])
        top_rep_ratio_user = await session.bot.get_group_member_info(group_id=grp_id, user_id=top_rep_ratio[0])

        msg += f"\n\n?????????????????????\n{most_msg_user['nickname']}({most_msg[0]})\n?????????{most_msg[1].total_msg}??????"
        msg += f"\n\n????????????????????????\n{most_rep_user['nickname']}({most_rep[0]})\n????????????{most_rep[1].total_rep}??????"
        t_stat = top_rep_ratio[1]
        msg += f"\n\n??????????????????????????????\n{top_rep_ratio_user['nickname']}({top_rep_ratio[0]})\n{t_stat.total_msg}??????????????????{t_stat.total_rep}?????????????????????{t_stat.rep_ratio}???"

    await session.send(msg, at_sender=True)
