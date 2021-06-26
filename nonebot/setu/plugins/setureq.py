import nonebot
from nonebot import on_command, CommandSession
import urllib
import json
@on_command('setu', aliases=['来一份涩图', '老鸭粉丝汤'], only_to_me=False)
async def _(session: CommandSession):
    arg = session.current_arg_text.strip().lower()
    if not arg:
        setu_data = await get_setu()
        await session.send(setu_data)
        await session.send("[CQ:image,file="+dlurl+"]")
        return
    setu_data = await get_setu(arg)
    await session.send(setu_data)
    await session.send("[CQ:image,file="+dlurl+"]")

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
        return "PID:"+pid+" 作者："+author+" 标题："+title+"\n标签："+tags+"\nURL:"+dlurl