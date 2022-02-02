import re
import os
import sys
import logging
from os import path

import qqconfig

import nonebot


log = logging.getLogger('mephisto-main')

if __name__ == '__main__':
    if qqconfig.ACCESS_TOKEN == '':
        log.warning("ACCESS_TOKEN is not set")

    if len(qqconfig.SUPERUSERS) == 0:
        log.warning("SUPERUSERS is not set")
    
    if qqconfig.API_ROOT == '':
        raise ValueError('API_ROOT is not set')

    plugins_folder = path.join(path.dirname(__file__), "mephisto", "plugins")
    sys.path.append(plugins_folder)
    print("plugins folder", plugins_folder)

    nonebot.init(qqconfig)

    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'mephisto', 'plugins'),
        'mephisto.plugins'
    )

    nonebot.run()
