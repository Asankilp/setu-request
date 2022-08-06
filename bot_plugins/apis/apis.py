import os
import json
import urllib.parse
import urllib.request

from seturequest import get_setu_from_loliconv1
async def togglesetuh():
    filename = 'setuhdisabled'
    if os.path.exists(filename) == True:
        os.remove(filename)
# lolicon
bakalist = [int, float, str, bool, dict, list, type(None)]

async def get_setu(arg: str) -> str:
    global dlurl
    p1, p2, p3 = arg.partition("&")  # 阻止用户自行添加参数
    data = get_setu_from_loliconv1(p1)
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
    data = get_setu_from_loliconv1(p1, r18=1)
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

def getconfig(key: str = None, default=bakalist):
    with open("setubot_config.json", mode="r", encoding="utf-8") as config:
        data = json.loads(config.read())
        if key is None:
            return data
        else:
            return data.get(str(key), default)
def setconfig(key: str, value: bakalist):
    if type(value) not in bakalist:
         print("Aaaaaaaaa")
    if key is None:
        data = value
    else:
        data = getconfig(default=dict())
        data[str(key)] = value
        print(data)
    try:
        with open("setubot_config.json", mode="w", encoding="utf-8") as config:
            text = json.dumps(data, indent=4, ensure_ascii=False)
            config.write(text)
            return True
    except:
        return False
    

