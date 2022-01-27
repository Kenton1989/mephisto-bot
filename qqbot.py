import re
from os import path
import logging

import nonebot

import qqconfig

l = logging.Logger("qqbot")

if __name__ == '__main__':

    if qqconfig.ACCESS_TOKEN == '':
        l.warn("ACCESS_TOKEN is not set")

    if len(qqconfig.SUPERUSERS):
        l.warn("SUPERUSERS is not set")

    nonebot.init(qqconfig)

    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'mephisto', 'plugins'),
        'mephisto.plugins'
    )

    nonebot.run()
