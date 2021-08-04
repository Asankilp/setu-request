'''
https://github.com/Asankilp/setu-request
----------------变量详情-----------------
ree：从涩图api拉取的数据
de：解码后的json
data：被代码搞过的json
dlurl：涩图url

pid：插画ID
pic：插画的p数
title：插画标题
uid：插画作者UID
author：插画作者
extname：扩展名

-----保存文件名自定义详细说明------
通过修改代码可以自定义保存的文件名。
于注释了 #拼接涩图文件名... 的代码处修改。
可以使用预先定义的变量，须遵循Python的语法。
格式例子：
pid + "_p" + pic + extname
    保存的文件名为"12345678_p0.png/jpg"
pid + "_" + author + extname
    保存的文件名为"12345678_插画作者.png/jpg"
*扩展名为必填项。也可以自定义扩展名。
*也可以使用高级语法。
'''
import urllib
import urllib.request
import urllib.parse
import requests
import json
import os
import re
import sys
from retrying import retry
@retry(stop_max_attempt_number=3, wait_fixed=3000)#自动重试
def download_img(dlurl): #定义下载函数
    global setudir
    extname = "." + dlurl.split(".").pop()
    setuname = pid + "_p" + pic + "-" + title + extname #拼接涩图文件名，可以使用变量自定义文件名，目前只可通过修改代码实现自定义
    setupath = os.path.join(setudir, setuname)
    if usecurl == True:
        if os.path.exists(setupath) is False:
            if os.system("curl "+dlurl+" -o "+setuname+" -#") == 0:
                print("\033[33m下载中...\033[0m")
                print("\033[32m下载完成\033[0m")
                return 'done'
            else:
                print("\033[31m发生错误！无法下载。\033[0m")
                return 'error'
        else:
            print ("文件已存在，跳过此下载。")
            return 'exist'
    else:
        r = requests.get(dlurl, stream=True)
        print("状态码：", r.status_code) # 返回状态码
        if r.status_code == 200:
            print("\033[33m下载中...\033[0m")
            if str(setudir) is None:#如果savedir.txt没内容，则取默认值
                setudir = "./"
            if os.path.exists(setupath) is False:
                open(os.path.join(setudir, setuname), 'wb').write(r.content) # 将内容写入图片
                print("\033[32m下载完成\033[0m")
                return 'done'
            else:
                print ("文件已存在，跳过此下载。")
                return 'exist'
        else:
            print("\033[31m发生错误！无法下载。\033[0m")
        del r
        return 'error'
def startdl(data):
    global arraycount, pid, pic, uid, title, author, dlurl
    for a in range(numb):
        #定义一大堆变量
        pid = str(data["data"][arraycount]["pid"])
        pic = str(data["data"][arraycount]["p"])
        uid = str(data["data"][arraycount]["uid"])
        title1 = str(data["data"][arraycount]["title"])
        author1 = str(data["data"][arraycount]["author"])
        title = replacesym(title1) #去除不能作为文件名的符号
        author = replacesym(author1)
        dlurl = data["data"][arraycount]["url"]
        tags = str(data["data"][arraycount]["tags"])
        print ("url:",dlurl)
        setuzhang = arraycount + 1#涩图张数
        print ("当前为第" + str(setuzhang) + "/" + str(numb) + "张涩图")
        print ("标题：" + title1 + " 作者：" + author1)
        print ("标签：" + tags);
        download_img(dlurl)#下载文件
        arraycount = arraycount + 1 #下载一张涩图后使数组顺序+1以便下载下一张涩图
def replacesym(zifu):
    spsymbol = ['\\',"|","/","?","<",">",":","*","\""]
    result = zifu.replace('\\', '')
    result = result.replace('/', '')
    result = result.replace('?', '？')
    result = result.replace('<', '')
    result = result.replace('>', '')
    result = result.replace(':', '：')
    result = result.replace('*', '')
    result = result.replace('|', '')
    result = result.replace('\"', '')
    return result
setufen = 0
debugmode = 0 #设为1时进入字符串替换调试模式，用于调试去除不能作为文件名的符号功能是否正常运行
if debugmode == 1:
    print("进入字符串替换调试模式。")
    replacedebug = replacesym(input("请输入字符串："))
    print ('替换后字符串：' + replacedebug)
    sys.exit(0)
if os.path.exists("savedir.txt") is False:#检测文件是否存在，若不存在则创建
    createdirr = open ("./savedir.txt", mode="a")
    createdirr.close()
dirr = open ("./savedir.txt", mode="r", encoding='utf-8')#打开文件
setudir = dirr.readline()
dirr.close()
if str(setudir) == "":
    showdir = os.getcwd()
else:
    showdir = setudir

if os.system("curl -V >nul") == 0:
    print("\033[32m已安装curl。将使用curl进行下载。\033[0m")
    usecurl = True
else:
    print("\033[33m未安装curl。将使用requests模块进行下载。\033[0m\n如果你已安装，请确认是否添加进环境变量。")
    usecurl = False
print ("正在使用Lolicon API v1。无需提供APIKEY。")
print ("在savedir.txt中可以输入自定义保存路径。")
print ("当前保存路径："+ str(showdir))
print ("为确保API运行正常，请勿请求过多涩图。")
count = int(input('来几份涩图？ ') or 1)
if count > 0:
        numb = int(input("一份几张涩图？（最大为100）") or 1)
        if numb > 0:
            word = urllib.parse.quote(input("搜索条件？（插画标题、作者、标签，留空则随机）"))#请求用户输入搜索条件+编码为url
            argu = str(input("其他参数？（参数之间用&分割，可留空）"))
            #word.encode('utf8','strict')
            for i in range(count): #循环（涩图份数）次
                ree = urllib.request.urlopen('https://api.lolicon.app/setu/v1/?keyword=' + word + '&num=' + str(numb) + "&" + argu) #从api获取json
                de = ree.read().decode() #解码
                print("返回JSON：",de)
                data = json.loads(de)
                code = int(data["code"])
                msg = str(data["msg"])
                #quota = (data['quota'])
                setufen = setufen + 1#涩图份数+1
                print ("当前为第" + str(setufen) + "/" + str(count) + "份涩图")
                arraycount = 0 #每次获取json时重置数组顺序
                if code == 0:
                    startdl(data)
                else:
                    print("\033[31m发生错误！代码：" + str(code) + "，错误信息：" + msg + "\033[0m")
                    break
        else:
            print("\033[31m张数无效。\033[0m")
else:
    print("\033[31m份数无效。\033[0m")
