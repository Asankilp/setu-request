import urllib.request, json, ssl, requests
ssl._create_default_https_context = ssl._create_unverified_context
def get_setu_from_loliconv1(keyword="", r18=0, num=1, proxy="i.pixiv.cat", size1200=False) -> dict:
    '''
    从Lolicon API v1获取涩图。将返回`dict`数据，格式与API返回json相同（详情参考[官方文档](https://api.lolicon.app/#/setu-v1) ） 。  
    参数：  
    * keyword (`str`) 搜索涩图的关键字。 
    * r18 (`int`) R18状态。`0`为非R18，`1`为R18，`2`为混合，默认为`0`。传递这些数字以外的参数会抛出`ValueError`异常。
    * num (`int`) 单次返回的涩图数量，默认为`1`。不得超过100，否则会抛出`ValueError`异常。
    * proxy (`str`) 返回的原图链接的域名，默认为`i.pixiv.cat`。为`disable`时返回真正的原图链接。
    * size1200 (`bool`) 是否使用长或宽最大为 1200px 的缩略图，默认为`False`。  

    '''
    R18_ALLOWED_ARG = [0,1,2]
    if r18 not in R18_ALLOWED_ARG:
        raise ValueError("'r18' argument can only be 0, 1 or 2")
    elif num <= 0:
        raise ValueError("'num' argument can only be <0 and >= 100")
    elif num > 100:
        raise ValueError("'num' argument can only be <0 and >= 100")
    response = urllib.request.urlopen(f"https://api.lolicon.app/setu/v1/?keyword={urllib.parse.quote(keyword)}&r18={r18}&num={num}&proxy={proxy}&size1200={str(size1200).lower()}")
    data = json.loads(response.read().decode())
    return data
def get_setu_from_loliconv2(keyword="", tag=[], r18=0, num=1, uid=None, size=["original"], proxy="i.pixiv.cat", dateAfter=None, dateBefore=None, dsc=False) -> dict:
    '''
    从Lolicon API v2获取涩图。将返回`dict`数据，格式与API返回json相同（详情参考[官方文档](https://api.lolicon.app/#/setu) ） 。  
    参数：  
    * keyword (`str`) 搜索涩图的关键字。 
    * tag (`list`) 返回匹配指定标签的作品（[详细说明](https://api.lolicon.app/#/setu?id=tag)）。
    * r18 (`int`) R18状态。`0`为非R18，`1`为R18，`2`为混合，默认为`0`。传递这些数字以外的参数会抛出`ValueError`异常。
    * num (`int`) 单次返回的涩图数量，默认为`1`。不得超过100，否则会抛出`ValueError`异常。
    * uid (`list`) 返回指定`uid`作者的作品，最多`20`个。
    * size (`list`) 返回指定图片规格的地址，默认为`["original"]`（[详细说明](https://api.lolicon.app/#/setu?id=size)）。
    * proxy (`str`) 设置图片地址所使用的在线反代服务，默认为`i.pixiv.cat`。为任意假值（如`false`, `0`, `null`）时返回真正的原图链接（[详细说明](https://api.lolicon.app/#/setu?id=proxy)）。
    * dateAfter (`int`) 返回在这个时间及以后上传的作品；时间戳，单位为毫秒。
    * dateBefore (`int`) 返回在这个时间及以前上传的作品；时间戳，单位为毫秒
    * dsc (`bool`) 禁用对某些缩写`keyword`和`tag`的自动转换，默认为`false`（[详细说明](https://api.lolicon.app/#/setu?id=dsc)）。
    '''
    global false, null, true
    false = null = true = ''
    requestjson = {
        "keyword": keyword,
        "tag": tag,
        "r18": r18,
        "num": num,
        "size": size,
        "proxy": proxy,
        "dsc": str(dsc).lower()
    }
    if uid is not None:
        requestjson["uid"] = uid
    if dateAfter is not None:
        requestjson["dateAfter"] = dateAfter
    if dateBefore is not None:
        requestjson["dateBefore"] = dateBefore
    print(requestjson)
    SIZE_ARGS = ["original", "regular", "small", "thumb", "mini"]
    R18_ALLOWED_ARG = [0,1,2]
    if r18 not in R18_ALLOWED_ARG:
        raise ValueError("'r18' argument can only be 0, 1 or 2")
    elif num <= 0:
        raise ValueError("'num' argument can only be <0 and >= 100")
    elif num > 100:
        raise ValueError("'num' argument can only be <0 and >= 100")
    for sizee in size:
        if sizee not in SIZE_ARGS:
            raise ValueError("'size' argument can only have 'original', 'regular', 'small', 'thumb', and 'mini'")
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url='https://api.lolicon.app/setu/v2', headers=headers, data=json.dumps(requestjson))
    response.encoding="utf-8"
    returnjson = response.content.decode('utf-8')
    return eval(returnjson)
def get_setu_from_fantasyzone(lib="pc", r18=0, not_proxy=False) -> str:
    '''
    从FantasyZone API获取图片。将返回图片URL（详情参考[官方文档](https://api.fantasyzone.cc/#/tu) ）。  
    参数：   
    * lib (`str`) 使用的图库，`pc`为横向动漫壁纸图片 ，`m`为纵向动漫壁纸图片，`mc`为FantasyZone Server截图，`pixiv`为pixiv库图片。传递这些以外的参数会抛出`ValueError`异常。
    * r18 (`int`) R18状态。`0`为非R18，`1`为R18，`2`为混合，默认为`0`，只能在图库为`pixiv`时生效。传递这些数字以外的参数会抛出`ValueError`异常。
    * not_proxy (`bool`) 是否关闭代理模式。默认为`False`。
    '''
    LIB_ALLOWED_ARG = ["pc","m","pixiv","mc"]
    R18_ALLOWED_ARG = [0,1,2]
    if lib not in LIB_ALLOWED_ARG:
        raise ValueError("'lib' argument can only be 'pc', 'm', 'pixiv' and 'mc'")
    elif r18 not in R18_ALLOWED_ARG:
        raise ValueError("'r18' argument can only be 0, 1 or 2")
    elif not_proxy == False:
        not_proxy = 0
    elif not_proxy == True:
        not_proxy = 1
    response = urllib.request.urlopen(f"http://api.fantasyzone.cc/tu/?class={lib}&r18={r18}&not_proxy={str(not_proxy).lower()}&type=url")
    rediecturl = str(response.geturl())
    return rediecturl