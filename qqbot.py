import re
import nonebot
from os import path

import qqconfig
if __name__ == '__main__':
    nonebot.init(qqconfig)
    
    # nonebot.load_builtin_plugins()
    
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'mephisto', 'plugins'),
        'mephisto.plugins'
    )

    nonebot.run()
