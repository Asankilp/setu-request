import seturequest
import os
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

usecurl = True
if os.path.exists("actions") is False:
    os.mkdir("actions")
setudir = "./actions"
def download_img(dlurl):
    global setudir, finishedcounter, failedcounter, skippedcounter
    extname = "." + dlurl.split(".").pop()
    setuname = pid + "_p" + pic + "-" + title + \
               extname
    setupath = os.path.join(setudir, setuname)
    if usecurl:
        if os.path.exists(setupath) is False:
            if str(setudir) is None:
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
data = seturequest.get_setu_from_loliconv1(num=10)
a = 0
for i in range(10):
    dlurl = data(["data"][a]["url"])
    pid = str(data["data"][a]["pid"])
    pic = str(data["data"][a]["p"])
    uid = str(data["data"][a]["uid"])
    title1 = str(data["data"][a]["title"])
    author1 = str(data["data"][a]["author"])
    title = replacesym(title1)  # 去除不能作为文件名的符号
    author = replacesym(author1)
    print(dlurl)
    download_img(dlurl)
    a = a + 1
