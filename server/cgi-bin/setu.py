import cgi, cgitb 
import urllib
import urllib.request
import urllib.parse
import requests
import json
# 创建 FieldStorage 的实例化
form = cgi.FieldStorage() 

arraycount = 0
# 获取数据
key = form.getvalue('apikey')
numb = form.getvalue('count')
word = form.getvalue('tiaojian')
argu = form.getvalue('arg')
if numb is None: 
    numb = 1
if key is None:
    key = ""
if word is None:
    word = ""
if argu is None:
    argu = ""
word = urllib.parse.quote(word)
print("Content-type:text/html")
print("\n\n")
print("<html>")
print("<head>")
print("<title>涩图请求</title>")
ree = urllib.request.urlopen('https://api.lolicon.app/setu/?keyword='+word+'&num='+str(numb)+'&apikey='+key+'&'+argu) #从api获取json
de = ree.read().decode() #解码
#print("返回JSON：",de)
data = json.loads(de)
code = int(data["code"])
msg = str(data["msg"])
quota = (data['quota'])
if code == 0:
    for a in range(int(numb)):
        pid = str(data["data"][arraycount]["pid"])
        dlurl = data["data"][arraycount]["url"]
        print("<img src="+dlurl+" alt="+pid+" width=500, height=500>")
        arraycount = arraycount + 1
print("</head>")
print("<body>")
