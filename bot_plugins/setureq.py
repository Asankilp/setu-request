import os
import re
import sys
import json
import urllib
import platform
import datetime
import urllib.parse

from nonebot import on_command, CommandSession, permission as perm
import nonebot.log as log
filename = 'setuhdisabled'
setu_bannedkeywords = []
setu_bannedtags = []
setu_h_bannedkeywords = []
setu_h_bannedtags = []
config = {
    "setu":{
        "banned_keywords":[],
        "banned_tags":[]
    },
    "setu-h":{
        "banned_keywords":[],
        "banned_tags":[]
    },
    "global":{
        "enable_url_logging": False
    }
}
clockstart = datetime.datetime.now()
log.logger.debug("机器人运行时间："+str(clockstart))
logfilename = f"{clockstart}.log"
setu_counter = 0
setub_counter = 0
setuc_counter = 0
setu_h_counter = 0
# 读取配置文件
if not os.path.exists("setubot_config.json"):
    log.logger.debug("setubot_config.json not found. Creating...")
    with open("setubot_config.json", mode="w") as newconf:
        newconf.writelines(json.dumps(config))
try:
    with open("setubot_config.json", encoding="utf-8") as conf:
        a = json.load(conf)
        setu_bannedkeywords = a['setu']['banned_keywords']
        setu_bannedtags = a['setu']['banned_tags']
        setu_h_bannedkeywords = a['setu-h']['banned_keywords']
        setu_h_bannedtags = a['setu-h']['banned_tags']
        global_enable_url_logging = a['global']['enable_url_logging']
except:
    log.logger.debug("Unable to read setubot_config.json.")
    pass
# 切换lolicon r18


@on_command('togglesetuh', only_to_me=False, permission=perm.SUPERUSER)
async def _(session: CommandSession):
    if os.path.exists(filename):
        os.remove(filename)
        await session.send("已启用/setu-h。")
    else:
        open(filename, mode='w')
        await session.send("已禁用/setu-h。")
# lolicon


@on_command('setu', aliases=['来一份涩图', '老鸭粉丝汤'], only_to_me=False)
async def _(session: CommandSession):
    global setu_counter
    arg = session.current_arg_text.strip()
    for i in setu_bannedkeywords:
        if re.search(i, arg) is not None:
            await session.send("此关键词已被屏蔽。")
            return
    await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
    setu_data = await get_setu(arg)
    if len(setu_data) == 5:
        for tag in setu_data[4]:
            if tag in setu_bannedtags:
                await session.send("API返回的涩图的其中一个或多个标签已被屏蔽。")
                return
        await url_log(setu_data[0])
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
    if os.path.exists(filename) is False:
        for i in setu_h_bannedkeywords:
            if re.search(i, arg) is not None:
                await session.send("此关键词已被屏蔽。")
                return
        await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
        setu_data = await get_setu_h(arg)
        if len(setu_data) == 5:
            for tag in setu_data[4]:
                if tag in setu_h_bannedtags:
                    await session.send("API返回的涩图的其中一个或多个标签已被屏蔽。")
                    return
            await url_log(setu_data[0])
            await session.send("PID:"+setu_data[1]+" 作者："+setu_data[2]+" 标题："+setu_data[3]+"\nURL:"+setu_data[0]+"\n*不会发送图片。")
            setu_h_counter = setu_h_counter + 1
        else:
            await session.send("代码："+setu_data[0]+"\n错误信息："+setu_data[1])
        del setu_data
# iw233


@on_command('setub', only_to_me=False)
async def _(session: CommandSession):
    global setub_counter
    await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
    a = urllib.request.urlopen("http://iw233.cn/api/Random.php")
    b = str(a.geturl())
    await url_log(b)
    await session.send("[CQ:image,file="+b+"]")
    setub_counter = setub_counter + 1
# fantasyzone


@on_command("setuc", only_to_me=False)
async def _(session: CommandSession):
    global setuc_counter
    await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
    data = urllib.request.urlopen("http://api.fantasyzone.cc/tu/?type=url")
    rediecturl = str(data.geturl())
    await url_log(rediecturl)
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
    /togglesetuh 切换/setu-h命令的可用性（启用/禁用）。对所有会话生效。仅超级用户可用。""")


@on_command("sendmsg", only_to_me=False, permission=perm.SUPERUSER)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.send("未指定消息。发送失败。")
    else:
        await session.send(arg)


async def togglesetuh():
    filename = 'setuhdisabled'
    if os.path.exists(filename) == True:
        os.remove(filename)
# lolicon


async def get_setu(arg="") -> str:
    global dlurl
    p1, p2, p3 = arg.partition("&")  # 阻止用户自行添加参数
    word = urllib.parse.quote(p1)
    ree = urllib.request.urlopen(
        'https://api.lolicon.app/setu/v1/?num=1&size1200=true&proxy=i.pixiv.re&keyword='+word)  # 从api获取json
    de = ree.read().decode()  # 解码
    data = json.loads(de)
    code = int(data["code"])
    msg = str(data["msg"])
    if code == 0:
        #quota = (data['quota'])
        dlurl = data["data"][0]["url"]
        pid = str(data["data"][0]["pid"])
        author = str(data["data"][0]["author"])
        title = str(data["data"][0]["title"])
        tags = list(data["data"][0]["tags"])
        return [dlurl, pid, author, title, tags]
    else:
        return [str(code), msg]
# lolicon r18


async def get_setu_h(arg="") -> str:
    global dlurl
    p1, p2, p3 = arg.partition("&")  # 阻止用户自行添加参数
    word = urllib.parse.quote(p1)
    ree = urllib.request.urlopen(
        'https://api.lolicon.app/setu/v1/?num=1&size1200=true&proxy=i.pixiv.re&r18=1&keyword='+word)  # 从api获取json
    de = ree.read().decode()  # 解码
    data = json.loads(de)
    code = int(data["code"])
    msg = str(data["msg"])
    if code == 0:
        #quota = (data['quota'])
        dlurl = data["data"][0]["url"]
        pid = str(data["data"][0]["pid"])
        author = str(data["data"][0]["author"])
        title = str(data["data"][0]["title"])
        tags = list(data["data"][0]["tags"])
        return [dlurl, pid, author, title, tags]
    else:
        return [str(code), msg]

async def url_log(url="") -> str:
    try:
        os.mkdir("setubot_urllog")
    except:
        pass
    if global_enable_url_logging == True:
        with open(os.path.join("setubot_urllog", logfilename), mode="a") as logfile:
            logfile.write(url+"\n")
            logfile.close()
                