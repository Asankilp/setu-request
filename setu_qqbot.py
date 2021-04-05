from typing import Optional
import requests
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import urllib
import urllib.parse
import json
import sys
import os

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
url="http://127.0.0.1:5700/send_group_msg"
version="1.4"

app = FastAPI()

class GroupItem(BaseModel):
    message: str
    group_id: int
class FriendMessage(BaseModel):
    message: str
    friend_id: int

if os.path.exists("apikey.txt") is False:#检测文件是否存在，若不存在则创建
    createkeyy = open ("./apikey.txt", mode="a")
    createkeyy.close()
keyy = open ("./apikey.txt", mode="r")#打开文件
key = keyy.readline()
keyy.close()
if str(key) == "":
    print ('你没有APIKEY。API调用次数与单次返回涩图张数将受限制。')
    apikey = False
else:
    print ("你的APIKEY：" + str(key))
    apikey = True
print ("如果你有APIKEY，请在apikey.txt中输入。")

@app.post("/")
async def create_item(item: dict):
    msg1=item.get("message")
    group=item.get("group_id")
    if msg1 and (msg1.startswith("来一份涩图") or (msg1.startswith("老鸭粉丝汤"))):
        print("收到了请求。")
        tiaojian = msg1[5:].strip()
        p1, p2 ,p3 = tiaojian.partition("&")#阻止用户自行添加参数
        word = urllib.parse.quote(p1)
        ree = urllib.request.urlopen('https://api.lolicon.app/setu/?apikey='+key+'&size1200=true&keyword='+word) #从api获取json
        de = ree.read().decode() #解码
        data = json.loads(de)
        code = int(data["code"])
        msg = str(data["msg"])
        if code == 0:
            quota = (data['quota'])
            dlurl = data["data"][0]["url"]
            pid = str(data["data"][0]["pid"])
            author = str(data["data"][0]["author"])
            title = str(data["data"][0]["title"])
            tags = str(data["data"][0]["tags"])
            requests.post(url,json={"group_id":group,"message":"PID:"+pid+" 作者："+author+" 标题："+title+"\n标签："+tags+"\n剩余调用次数："+str(quota)+"\nURL:"+dlurl+"[CQ:image,file="+dlurl+",url="+dlurl+"]"})
            print("完成了请求。")
        else:
            requests.post(url,json={"group_id":group,"message":"代码："+str(code)+"\n错误信息："+msg})
        del tiaojian
        del word
    if msg1=="ver":
        requests.post(url,json={"group_id":group,"message":"setu_qqbot（https://github.com/Asankilp/setu-request） ver"+version+"\n本机器人基于uvicorn及go-cqhttp（github.com/Mrs4s/go-cqhttp）。涩图API为Lolicon API（api.lolicon.app）。\n提供了APIKEY："+str(apikey)+"\n运行环境：\nPython "+sys.version})
    if msg1=="目力":
        requests.post(url,json={"group_id":group,"message":"[CQ:record,file=https://asankilp.github.io/muli.mp3]"})
    return {}

