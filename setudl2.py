from retrying import retry
import requests
import json
import os
import seturequest

config = {
    "force_requests": False,
    "save_dir": ""
    }
if not os.path.exists("config.json"):
    print("找不到config.json。正在创建...")
    with open("config.json", mode="w") as newconf:
        newconf.writelines(json.dumps(config))
try:
    with open("config.json", encoding="utf-8") as conf:
        a = json.load(conf)
        force_requests = a["force_requests"]
        setudir = a["save_dir"]
except:
    print("无法读取config.json.")
    pass
if setudir == "":
    showdir = os.getcwd()
else:
    showdir = setudir


@retry(stop_max_attempt_number=3, wait_fixed=3000)  # 自动重试
def download_img(dlurl):  # 定义下载函数
    global setudir, finishedcounter, failedcounter, skippedcounter
    extname = "." + dlurl.split(".").pop()
    setuname = pid + "_p" + pic + "-" + title + \
               extname  # 拼接涩图文件名，可以使用变量自定义文件名，目前只可通过修改代码实现自定义
    setupath = os.path.join(setudir, setuname)
    if usecurl:
        if os.path.exists(setupath) is False:
            if str(setudir) is None:  # 如果savedir.txt没内容，则取默认值
                setudir = "./"
            print("\033[33m下载中...\033[0m")
            if os.system("curl " + dlurl + " -o " + "\"" + os.path.join(setudir, setuname) + "\"" + " -#") == 0:
                print("\033[32m下载完成\033[0m")
                finishedcounter = finishedcounter + 1
                return 'done'
            else:
                print("\033[31m发生错误！无法下载。\033[0m")
                failedcounter = failedcounter + 1
                return 'error'
        else:
            print("文件已存在，跳过此下载。")
            skippedcounter = skippedcounter + 1
            return 'exist'
    else:
        r = requests.get(dlurl, stream=True)
        print("状态码：", r.status_code)  # 返回状态码
        if r.status_code == 200:
            print("\033[33m下载中...\033[0m")
            if str(setudir) is None:  # 如果savedir为空，则取默认值
                setudir = "./"
            if os.path.exists(setupath) is False:
                open(os.path.join(setudir, setuname),
                     'wb').write(r.content)  # 将内容写入图片
                print("\033[32m下载完成\033[0m")
                finishedcounter = finishedcounter + 1
                return 'done'
            else:
                print("文件已存在，跳过此下载。")
                skippedcounter = skippedcounter + 1
                return 'exist'
        else:
            print("\033[31m发生错误！无法下载。\033[0m")
        del r
        failedcounter = failedcounter + 1
        return 'error'

def startdl(data):
    global arraycount, pid, pic, uid, title, author, dlurl
    realcount = len(data)
    if realcount < numb:
        print(f"\033[33m返回的涩图数量（{realcount}）少于指定的涩图数量（{numb}）。\033[0m")
    for a in range(realcount):
        # 定义一大堆变量
        pid = str(data[arraycount]["pid"])
        pic = str(data[arraycount]["p"])
        uid = str(data[arraycount]["uid"])
        title1 = str(data[arraycount]["title"])
        author1 = str(data[arraycount]["author"])
        title = replacesym(title1)  # 去除不能作为文件名的符号
        author = replacesym(author1)
        dlurl = list(dict(data[arraycount]["urls"]).values())[0]
        tags = str(data[arraycount]["tags"])
        aitype = int(data[arraycount]["aiType"])
        print("url:", dlurl)
        print(f"主站URL:https://pixiv.net/i/{pid}")
        if aitype == 2:
            print("\033[33m这是 AI 生成的作品。\033[0m")
        setuzhang = arraycount + 1  # 涩图张数
        print(f"当前为第{str(setuzhang)}/{str(realcount)}张涩图")
        print(f"标题：{title1} 作者：{author1}")
        print("标签：" + tags)
        download_img(dlurl)  # 下载文件
        arraycount = arraycount + 1  # 下载一张涩图后使数组顺序+1以便下载下一张涩图

if os.name == 'nt':
    null = "nul"
elif os.name == 'posix':
    null = "/dev/null"


if os.system(f"curl -V >> {null}") == 0 and force_requests == False:  # what the fuck
    print("\033[32m已安装curl。将使用curl进行下载。\033[0m")
    usecurl = True
else:
    print("\033[33m未安装curl。将使用requests模块进行下载。\033[0m\n如果你已安装，请确认是否添加进环境变量。")
    usecurl = False


def replacesym(zifu):
    # spsymbol = ['\\',"|","/","?","<",">",":","*","\""]
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
finishedcounter = 0
failedcounter = 0
skippedcounter = 0
inputtags = []

def main():
    global numb, arraycount, setufen
    print("正在使用Lolicon API v2。")
    print("在config.json中可以输入自定义保存路径。")
    print(f"当前保存路径：{str(showdir)}")
    count = int(input('来几份涩图？ ') or 1)
    if count > 0:
        numb = int(input("一份几张涩图？（最大为20）") or 1)
        if numb > 0:
            print("搜索条件？（标签、作者名、标题，大小写不敏感）")
            print("\033[33m请在\">\"提示符后输入搜索条件，使用\"|\"符号表示OR。\n输入完毕或不需要搜索条件时，在不输入任何字符的情况下回车。\033[0m")
            tagcount = 1
            while True:
                tagstr = str(input(f"{tagcount}>"))
                tagcount = tagcount + 1
                if tagstr == "":
                    print(inputtags)
                    break
                else:
                    inputtags.append(tagstr)
            r18 = int(input("R18状态（0为禁用，1为启用，2为混合）") or 0)
            size = str(input("图片尺寸（可能的值：original|regular|small|thumb|mini） (original)"))
            blockAI = bool(input("是否排除 AI 生成作品？(y/N)") or False)
            for i in range(count):  # 循环（涩图份数）次
                data = seturequest.get_setu_from_loliconv2(
                    tag=inputtags, num=numb, r18=r18,excludeAI=blockAI, size=size)  # 从api获取json
                print("返回JSON：", data)
                error = (data["error"])
                setufen = setufen + 1  # 涩图份数+1
                print(f"当前为第{str(setufen)}/{str(count)}份涩图")
                arraycount = 0  # 每次获取json时重置数组顺序
                if error == "":
                    startdl(data["data"])
                else:
                    print(f"\033[31m发生错误！错误信息：{error}\033[0m")
                    break
            print(
                f"\033[32m所有下载已完成。\033[0m\n成功：{finishedcounter}，失败：{failedcounter}，跳过：{skippedcounter}")
        else:
            print("\033[31m张数无效。\033[0m")
    else:
        print("\033[31m份数无效。\033[0m")

if __name__ == "__main__":
    main()