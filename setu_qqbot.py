from typing import Optional
import requests
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import urllib
import urllib.parse
import json
import sys

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
url="http://127.0.0.1:5700/send_group_msg"
version="1.3"

app = FastAPI()

class GroupItem(BaseModel):
    message: str
    group_id: int
class FriendMessage(BaseModel):
    message: str
    friend_id: int

@app.post("/")
async def create_item(item: dict):
    msg1=item.get("message")
    group=item.get("group_id")
    if msg1 and (msg1.startswith("来一份涩图")):
        tiaojian = msg1[5:].strip()
        word = urllib.parse.quote(tiaojian)
        ree = urllib.request.urlopen('https://api.lolicon.app/setu/?keyword='+word) #从api获取json
        de = ree.read().decode() #解码
        data = json.loads(de)
        quota = (data['quota'])
        dlurl = data["data"][0]["url"]
        pid = str(data["data"][0]["pid"])
        author = str(data["data"][0]["author"])
        title = str(data["data"][0]["title"])
        tags = str(data["data"][0]["tags"])
        requests.post(url,json={"group_id":group,"message":"PID:"+pid+" 作者："+author+" 标题："+title+"\n标签："+tags+"\n剩余调用次数："+str(quota)+"\nURL:"+dlurl+"[CQ:image,file="+dlurl+",url="+dlurl+"]"})
        del tiaojian
        del word
    if msg1=="ver":
        requests.post(url,json={"group_id":group,"message":"涩图机器人 ver"+version+" by Asankilp\n本机器人基于uvicorn及go-cqhttp(github.com/Mrs4s/go-cqhttp)。\n涩图请求核心代码来自Asankilp的 涩图下载 脚本。\n运行环境：\nPython "+sys.version})
    if msg1=="目力":
        requests.post(url,json={"group_id":group,"message":"[CQ:record,file=https://asankilp.github.io/muli.mp3]"})
    return {}

