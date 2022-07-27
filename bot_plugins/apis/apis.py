import os
import json
import urllib
import urllib.parse
import urllib.request
async def togglesetuh():
    filename = 'setuhdisabled'
    if os.path.exists(filename) == True:
        os.remove(filename)
# lolicon
bakalist = [int, float, str, bool, dict, list, type(None)]

async def get_setu(arg: str) -> str:
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


async def get_setu_h(arg: str) -> str:
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

async def url_log(url: str, logfilename: str) -> str:
    try:
        os.mkdir("setubot_urllog")
    except:
        pass
    with open(os.path.join("setubot_urllog", logfilename), mode="a") as logfile:
        logfile.write(url+"\n")
        logfile.close()

async def getconfig(key: str, default=bakalist):
    with open("setubot_config.json", mode="r", encoding="utf-8") as config:
        data = json.loads(config.read())
        if key is None:
            return data
        else:
            return data.get(str(key), default)
async def setconfig(key: str, value: bakalist):
    if type(value) not in bakalist:
         return False
    if key is None:
        data = value
    else:
        data = getconfig(default=dict())
        data[str(key)] = value
    try:
        with open("setubot_config.json", mode="w", encoding="utf-8") as config:
            text = json.dumps(data, indent=4, ensure_ascii=False)
            config.write(text)
            return True
    except:
        return False
    

