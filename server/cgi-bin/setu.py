#! /usr/bin/env python3
import cgi
import urllib
import urllib.request
import urllib.parse
import json
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
# 创建 FieldStorage 的实例化
form = cgi.FieldStorage() 

arraycount = 0
# 获取数据
#key = form.getvalue('apikey')
numb = form.getvalue('count')
word = form.getvalue('tiaojian')
argu = form.getvalue('arg')
if numb is None: 
    numb = 1
if word is None:
    word = ""
if argu is None:
    argu = ""
word = urllib.parse.quote(word)
print("Content-type:text/html")
print("\n\n")
print("<html>")
print("<head>")
print("<meta charset=\"utf-8\">")
print("<title>涩图请求</title>")
print("</head>")
print("<body>")
ree = urllib.request.urlopen(f'https://api.lolicon.app/setu/v1/?keyword={word}&num={str(numb)}&{argu}') #从api获取json
de = ree.read().decode() #解码
#print("返回JSON：",de)
data = json.loads(de)
code = int(data["code"])
msg = str(data["msg"])
#quota = (data['quota'])
if code == 0:
    #print("<a>剩余调用次数："+str(quota)+"</a> <br/>")
    for a in range(int(numb)):
        pid = str(data["data"][arraycount]["pid"])
        title = str(data["data"][arraycount]["title"])
        tags = str(data["data"][arraycount]["tags"])
        author = str(data["data"][0]["author"])
        dlurl = data["data"][arraycount]["url"]
        print(f"URL:<a href=\"{dlurl}\">{dlurl} <a> PID:{pid} 作者:{author} 标题:{title} 标签:{tags}")
        print(f"<img src={dlurl} alt={pid} width=500, height=500> <br/>")
        arraycount = arraycount + 1
else:
    print("代码："+str(code)+" 错误信息："+msg)
print("</body>")
print("<html>")
