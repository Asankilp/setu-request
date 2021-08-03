import os
conf = [
'from nonebot.default_config import *\n',
'HOST = \'127.0.0.1\'\n',
'PORT = 8000\n',
'API_ROOT = \'http://127.0.0.1:5700\'\n'
]
if os.path.exists('config.py') is False:
    print('config.py not found. Creating...')
    with open('config.py',mode='a') as newconf:
        newconf.writelines(conf)
import nonebot
import config
from os import path
if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'setu', 'plugins'),
        'setu.plugins'
    )
    nonebot.run()