import urllib.request, json, ssl
ssl._create_default_https_context = ssl._create_unverified_context
def get_setu_from_loliconv1(keyword="", r18=0, num=1, proxy="i.pixiv.cat", size1200=False):
    r18_allowed_arg = [0,1,2]
    if r18 not in r18_allowed_arg:
        raise ValueError("r18 argument can only be 0, 1 or 2")
    elif num <= 0:
        raise ValueError("num argument can only be <0 and >= 100")
    elif num > 100:
        raise ValueError("num argument can only be <0 and >= 100")
    response = urllib.request.urlopen(f"https://api.lolicon.app/setu/v1/?keyword={urllib.parse.quote(keyword)}&r18={r18}&num={num}&proxy={proxy}&size1200={str(size1200).lower()}")
    data = json.loads(response.read().decode())
    return data
def get_setu_from_fantasyzone(lib="pc", r18=0, not_proxy=False):
    lib_allowed_arg = ["pc","m","pixiv","mc"]
    r18_allowed_arg = [0,1,2]
    if lib not in lib_allowed_arg:
        raise ValueError("lib argument can only be pc, m, pixiv and mc")
    elif r18 not in r18_allowed_arg:
        raise ValueError("r18 argument can only be 0, 1 or 2")
    elif not_proxy == False:
        not_proxy = 0
    elif not_proxy == True:
        not_proxy = 1
    response = urllib.request.urlopen(f"http://api.fantasyzone.cc/tu/?class={lib}&r18={r18}&not_proxy={not_proxy}&type=url")
    rediecturl = str(response.geturl())
    return rediecturl