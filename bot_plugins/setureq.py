import os
import re
import sys
import json
import urllib
import traceback
import platform
import datetime
import urllib.parse
from anyio import run_async_from_thread
from requests import JSONDecodeError

from bot_plugins.apis.apis import *
from nonebot import on_command, CommandSession, permission as perm
import nonebot.log as log
def setues_is_enable(sender: perm.SenderRoles):
    if getconfig("setues_enable") is True:
        return True
    else:
        return False
config = {
    "setues_enable": True,
    "setu_h_enable": False,
    "enable_url_logging": False
}
clockstart = datetime.datetime.now()
log.logger.debug("机器人运行时间："+str(clockstart))
logfilename = f"{clockstart}.log"
setu_counter = 0
setub_counter = 0
setuc_counter = 0
setu_h_counter = 0
def force_create_config():
    with open("setubot_config.json", mode="w") as newconf:
        newconf.writelines(json.dumps(config, indent=4))
# 读取配置文件
if not os.path.exists("setubot_config.json"):
    log.logger.debug("setubot_config.json不存在。 正在创建...")
    force_create_config()
try:
    for key in config:
        if json.loads(open("setubot_config.json", encoding="utf-8").read()).get(key) is None:
            result = setconfig(key=key, value=config[key])
            log.logger.debug("发现配置文件未写入的键值对，已自动写入："+key+": "+str(config[key]))
            log.logger.debug(str(result))
except json.decoder.JSONDecodeError:
    log.logger.debug("setubot_config.json 读取失败，已自动重置")
    force_create_config()
    sys.exit(-1)
# 切换涩图命令


@on_command('togglesetues', only_to_me=False, permission=perm.SUPERUSER)
async def _(session: CommandSession):
    if getconfig("setues_enable") is True:
        setconfig(key="setues_enable", value=False)
        await session.send("不可以涩涩")
    elif getconfig("setues_enable") is False:
        setconfig(key="setues_enable", value=True)
        await session.send("可以涩涩")
# 切换lolicon r18
@on_command("togglesetuh", only_to_me=False, permission=perm.SUPERUSER)
async def _(session: CommandSession):
    if getconfig("setu_h_enable") is True:
        setconfig(key="setu_h_enable", value=False)
        await session.send("不可以色色")
    elif getconfig("setu_h_enable") is False:
        setconfig(key="setu_h_enable", value=True)
        await session.send("可以色色")
# lolicon
@on_command('setu', aliases=['来一份涩图', '老鸭粉丝汤'], only_to_me=False, permission=setues_is_enable)
async def _(session: CommandSession):
    global setu_counter
    arg = session.current_arg_text.strip()
    await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
    setu_data = await get_setu(arg)
    if len(setu_data) == 5:
        if getconfig("enable_url_logging") == True: await url_log(setu_data[0], logfilename=logfilename)
        await session.send("PID:"+setu_data[1]+" 作者："+setu_data[2]+" 标题："+setu_data[3]+"\n标签："+str(setu_data[4])+"\nURL:"+setu_data[0])
        await session.send("[CQ:image,file="+setu_data[0]+"]")
        setu_counter = setu_counter + 1
    else:
        await session.send("代码："+setu_data[0]+"\n错误信息："+setu_data[1])
    del setu_data
# lolicon r18


@on_command('setu-h', only_to_me=False)
async def _(session: CommandSession):
    global setu_h_counter
    arg = session.current_arg_text.strip()
    if getconfig("setu_h_enable") is True: #setuh_enable
        await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
        setu_data = await get_setu_h(arg)
        if len(setu_data) == 5:
            for tag in setu_data[4]:
                if tag in setu_h_bannedtags:
                    await session.send("API返回的涩图的其中一个或多个标签已被屏蔽。")
                    return
            if getconfig("enable_url_logging") == True: await url_log(setu_data[0], logfilename=logfilename)
            await session.send("PID:"+setu_data[1]+" 作者："+setu_data[2]+" 标题："+setu_data[3]+"\nURL:"+setu_data[0]+"\n*不会发送图片。")
            setu_h_counter = setu_h_counter + 1
        else:
            await session.send("代码："+setu_data[0]+"\n错误信息："+setu_data[1])
        del setu_data
    else:
        await session.send("不可以色色！")
# iw233


@on_command('setub', only_to_me=False, permission=setues_is_enable)
async def _(session: CommandSession):
    global setub_counter
    await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
    a = urllib.request.urlopen("http://iw233.cn/api/Random.php")
    b = str(a.geturl())
    if getconfig("enable_url_logging") == True: await url_log(b, logfilename=logfilename)
    await session.send("[CQ:image,file="+b+"]")
    setub_counter = setub_counter + 1
# fantasyzone


@on_command("setuc", only_to_me=False, permission=setues_is_enable)
async def _(session: CommandSession):
    global setuc_counter
    await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
    data = urllib.request.urlopen("http://api.fantasyzone.cc/tu/?type=url")
    rediecturl = str(data.geturl())
    if getconfig("enable_url_logging") == True: await url_log(rediecturl, logfilename=logfilename)
    await session.send("[CQ:image,file="+rediecturl+"]")
    setuc_counter = setuc_counter + 1


@on_command("ver", only_to_me=False)
async def _(session: CommandSession):
    await session.send(f"""setu_qqbot（https://github.com/Asankilp/setu-request）
    本机器人基于NoneBot。涩图API为Lolicon API v1（api.lolicon.app）。
    运行环境：
    Python {sys.version}
    操作系统：
    {platform.platform()} {platform.version()}
    总运行时间：
    {datetime.datetime.now() - clockstart}
    /setu   成功次数：{setu_counter}
    /setu-h 成功次数：{setu_h_counter}
    /setub  成功次数：{setub_counter}
    /setuc  成功次数：{setuc_counter}""")


@on_command("muli", aliases=['目力', '嚎叫'], only_to_me=False)
async def _(session: CommandSession):
    await session.send("[CQ:record,file=https://asankilp.github.io/muli.mp3]")


@on_command("help", only_to_me=False)
async def _(session: CommandSession):
    await session.send("""用法：
    /setu [关键词] 从Lolicon API模糊搜索插画标题，作者，标签的涩图。未提供关键词将随机搜索。
    /setub 从 https://iw233.cn/ 的API（http://iw233.cn/api/Random.php）随机获取涩图。
    /setuc 从FantasyZone API（https://api.fantasyzone.cc/#/tu）随机获取涩图。
    /setu-h [关键词] 从Lolicon API模糊搜索插画标题，作者，标签的涩图(R-18)。未提供关键词将随机搜索。
    /ver 查看Bot信息
    /sendmsg <消息> 使此机器人发送指定的消息。仅超级用户可用。
    /togglesetuh 切换/setu-h命令的可用性（启用/禁用）。对所有会话生效。仅超级用户可用。
    /togglesetues 切换除/setu-h外所有请求涩图命令的可用性（启用/禁用）。对所有会话生效。仅超级用户可用。
    /getconfig <key> 获取在setubot_config.json中指定键的值。仅超级用户可用。""")


@on_command("sendmsg", only_to_me=False, permission=perm.SUPERUSER)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.send("未指定消息。发送失败。")
    else:
        await session.send(arg)

@on_command("getconfig", permission=perm.SUPERUSER, only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    result = getconfig(arg)
    await session.send(str(result))