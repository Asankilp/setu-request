import os
conf = [
'from nonebot.default_config import *\n',
'HOST = \'127.0.0.1\'\n',
'PORT = 8000\n',
'API_ROOT = \'http://127.0.0.1:5700\'\n'
]
if os.path.exists('bot_config.py') is False:
    print('bot_config.py not found. Creating...')
    with open('bot_config.py',mode='a') as newconf:
        newconf.writelines(conf)
import nonebot
import bot_config
from os import path
if __name__ == '__main__':
    nonebot.init(bot_config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'bot_plugins'),
        'bot_plugins'
    )
    nonebot.run()
