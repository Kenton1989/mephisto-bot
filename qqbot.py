import re
import os
import sys
import logging
from os import path

import nonebot

import qqconfig

if __name__ == '__main__':
    if qqconfig.ACCESS_TOKEN == '':
        nonebot.logger.warning("ACCESS_TOKEN is not set")

    if len(qqconfig.SUPERUSERS) == 0:
        nonebot.logger.warning("SUPERUSERS is not set")
        
    plugins_folder = path.join(path.dirname(__file__),"mephisto", "plugins")
    sys.path.append(plugins_folder)
    print("plugins folder", plugins_folder)

    nonebot.init(qqconfig)

    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'mephisto', 'plugins'),
        'mephisto.plugins'
    )

    nonebot.run()
