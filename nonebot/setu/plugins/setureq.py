import nonebot
from nonebot import on_command, CommandSession, permission as perm
import urllib
import urllib.parse
import json
import sys
import platform

from requests.sessions import Session, session
@on_command('setu', aliases=['来一份涩图', '老鸭粉丝汤'], only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
        setu_data = await get_setu()
        if len(setu_data) == 5:
            await session.send("PID:"+setu_data[1]+" 作者："+setu_data[2]+" 标题："+setu_data[3]+"\n标签："+setu_data[4]+"\nURL:"+setu_data[0])
            await session.send("[CQ:image,file="+setu_data[0]+"]")
        else:
            await session.send("代码："+setu_data[0]+"\n错误信息："+setu_data[1])
        del setu_data
    else:
        await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
        setu_data = await get_setu(arg)
        if len(setu_data) == 5:
            await session.send("PID:"+setu_data[1]+" 作者："+setu_data[2]+" 标题："+setu_data[3]+"\n标签："+setu_data[4]+"\nURL:"+setu_data[0])
            await session.send("[CQ:image,file="+setu_data[0]+"]")
        else:
            await session.send("代码："+setu_data[0]+"\n错误信息："+setu_data[1])
        del setu_data
@on_command('setu-h', only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
        setu_data = await get_setu_h()
        if len(setu_data) == 5:
            await session.send("PID:"+setu_data[1]+" 作者："+setu_data[2]+" 标题："+setu_data[3]+"\nURL:"+setu_data[0]+"\n*不会发送图片。")
        else:
            await session.send("代码："+setu_data[0]+"\n错误信息："+setu_data[1])
        del setu_data
    else:
        await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
        setu_data = await get_setu_h(arg)
        if len(setu_data) == 5:
            await session.send("PID:"+setu_data[1]+" 作者："+setu_data[2]+" 标题："+setu_data[3]+"\nURL:"+setu_data[0]+"\n*不会发送图片。")
        else:
            await session.send("代码："+setu_data[0]+"\n错误信息："+setu_data[1])
        del setu_data
@on_command('setub', only_to_me=False)
async def _(session: CommandSession):
    await session.send("搜索涩图中。请耐心等待。\n一段时间后仍未响应，请重试或联系Bot管理员。")
    setu_data = get_setub()
    await session.send("[CQ:image,file="+setu_data+"]")
@on_command("ver", only_to_me=False)
async def _(session: CommandSession):
    await session.send("setu_qqbot（https://github.com/Asankilp/setu-request）\n本机器人基于NoneBot。涩图API为Lolicon API v1（api.lolicon.app）。\n运行环境：\nPython "+sys.version+"\n操作系统：\n"+platform.platform()+" "+platform.version())
@on_command("muli", aliases=['目力', '嚎叫'], only_to_me=False)
async def _(session: CommandSession):
    await session.send("[CQ:record,file=https://asankilp.github.io/muli.mp3]")
@on_command("help", only_to_me=False)
async def _(session: CommandSession):
    await session.send("用法：\n/setu [关键词] 从Lolicon API模糊搜索插画标题，作者，标签的涩图。未提供关键词将随机搜索。\n/setub 从 https://iw233.cn/ 的API（http://iw233.cn/api/Random.php）随机获取涩图。\n/setu-h [关键词] 从Lolicon API模糊搜索插画标题，作者，标签的涩图(R-18)。未提供关键词将随机搜索。\n/ver 查看Bot信息\n/sendmsg <消息> 使此机器人发送指定的消息。仅超级用户可用。")
@on_command("sendmsg", only_to_me=False, permission=perm.SUPERUSER)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip()
    if not arg:
        await session.send("未指定消息。发送失败。")
    else:
        await session.send(arg)
async def get_setu(arg="") -> str:
    global dlurl
    p1, p2 ,p3 = arg.partition("&")#阻止用户自行添加参数
    word = urllib.parse.quote(p1)
    ree = urllib.request.urlopen('https://api.lolicon.app/setu/v1/?size1200=true&keyword='+word) #从api获取json
    de = ree.read().decode() #解码
    data = json.loads(de)
    code = int(data["code"])
    msg = str(data["msg"])
    if code == 0:
        #quota = (data['quota'])
        dlurl = data["data"][0]["url"]
        pid = str(data["data"][0]["pid"])
        author = str(data["data"][0]["author"])
        title = str(data["data"][0]["title"])
        tags = str(data["data"][0]["tags"])
        return [dlurl, pid, author, title, tags]
    else:
        return [str(code), msg]
async def get_setu_h(arg="") -> str:
    global dlurl
    p1, p2 ,p3 = arg.partition("&")#阻止用户自行添加参数
    word = urllib.parse.quote(p1)
    ree = urllib.request.urlopen('https://api.lolicon.app/setu/v1/?size1200=true&r18=1&keyword='+word) #从api获取json
    de = ree.read().decode() #解码
    data = json.loads(de)
    code = int(data["code"])
    msg = str(data["msg"])
    if code == 0:
        #quota = (data['quota'])
        dlurl = data["data"][0]["url"]
        pid = str(data["data"][0]["pid"])
        author = str(data["data"][0]["author"])
        title = str(data["data"][0]["title"])
        tags = str(data["data"][0]["tags"])
        return [dlurl, pid, author, title, tags]
    else:
        return [str(code), msg]
def get_setub():
    a = urllib.request.urlopen("http://iw233.cn/api/Random.php")
    b = str(a.geturl())
    return b