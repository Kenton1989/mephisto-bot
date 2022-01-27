import re
import os
import sys
import logging
from os import path

import nonebot

import qqconfig

l = logging.Logger("qqbot")

if __name__ == '__main__':
    if qqconfig.ACCESS_TOKEN == '':
        l.warning("ACCESS_TOKEN is not set")

    if len(qqconfig.SUPERUSERS) == 0:
        l.warning("SUPERUSERS is not set")
    else:
        owners = ":".join(str(id) for id in qqconfig.SUPERUSERS)
        os.environ["QQ_BOT_SU"] = owners
        
    plugins_folder = path.join(path.dirname(__file__),"mephisto", "plugins")
    sys.path.append(plugins_folder)
    print("plugins folder", plugins_folder)

    nonebot.init(qqconfig)

    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'mephisto', 'plugins'),
        'mephisto.plugins'
    )

    nonebot.run()
