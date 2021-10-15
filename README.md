# setu-request
涩图的请求与下载。（服务由[Lolicon API](http://api.lolicon.app)等提供）
## QQ机器人  
`setu_qqbot.py`可通过uvicorn运行服务器，通过[go-cqhttp](http://github.com/Mrs4s/go-cqhttp)或其他遵循[OneBot 标准](https://github.com/howmanybots/onebot)的机器人库来对QQ机器人提供支持。  
使用[NoneBot](https://github.com/nonebot/nonebot)框架的机器人位于[该目录](nonebot)下。运行`run.py`并通过[go-cqhttp](http://github.com/Mrs4s/go-cqhttp)或其他遵循[OneBot 标准](https://github.com/howmanybots/onebot)的机器人库来对QQ机器人提供支持。
## web 版本
web 版本可通过运行`server/run.py`开启简易服务器，并通过指定的端口在浏览器访问。  
## 调用函数
`seturequest.py`包含了可供调用的封装函数。  
### 函数说明
```python
get_setu_from_loliconv1(keyword="", r18=0, num=1, proxy="i.pixiv.cat", size1200=False)
```
从Lolicon API v1获取涩图。将返回`dict`数据，格式与API返回json相同（详情参考[官方文档](https://api.lolicon.app/#/setu-v1) ） 。  
参数：  
* __keyword__ (`str`) 搜索涩图的关键字。 
* __r18__ (`int`) R18状态。`0`为非R18，`1`为R18，`2`为混合，默认为`0`。传递这些数字以外的参数会抛出`ValueError`异常。
* __num__ (`int`) 单次返回的涩图数量，默认为`1`。不得超过100，否则会抛出`ValueError`异常。
* __proxy__ (`str`) 返回的原图链接的域名，默认为`i.pixiv.cat`。为`disable`时返回真正的原图链接。
* __size1200__ (`bool`) 是否使用长或宽最大为 1200px 的缩略图，默认为`False`。  
```python
get_setu_from_loliconv2(keyword="", tag=[], r18=0, num=1, uid=None, size=["original"], proxy="i.pixiv.cat", dateAfter=None, dateBefore=None, dsc=False)
```
从Lolicon API v2获取涩图。将返回`dict`数据，格式与API返回json相同（详情参考[官方文档](https://api.lolicon.app/#/setu) ） 。  
参数：  
* __keyword__ (`str`) 搜索涩图的关键字。 
* __tag__ (`list`) 返回匹配指定标签的作品（[详细说明](https://api.lolicon.app/#/setu?id=tag)）。
* __r18__ (`int`) R18状态。`0`为非R18，`1`为R18，`2`为混合，默认为`0`。传递这些数字以外的参数会抛出`ValueError`异常。
* __num__ (`int`) 单次返回的涩图数量，默认为`1`。不得超过100，否则会抛出`ValueError`异常。
* __uid__ (`list`) 返回指定`uid`作者的作品，最多`20`个。
* __size__ (`list`) 返回指定图片规格的地址，默认为`["original"]`（[详细说明](https://api.lolicon.app/#/setu?id=size)）。
* __proxy__ (`str`) 设置图片地址所使用的在线反代服务，默认为`i.pixiv.cat`。为任意假值（如`false`, `0`, `null`）时返回真正的原图链接（[详细说明](https://api.lolicon.app/#/setu?id=proxy)）。
* __dateAfter__ (`int`) 返回在这个时间及以后上传的作品；时间戳，单位为毫秒。
* __dateBefore__ (`int`) 返回在这个时间及以前上传的作品；时间戳，单位为毫秒
* __dsc__ (`bool`) 禁用对某些缩写`keyword`和`tag`的自动转换，默认为`false`（[详细说明](https://api.lolicon.app/#/setu?id=dsc)）。
```python
get_setu_from_fantasyzone(lib="pc", r18=0, not_proxy=False)
```
从FantasyZone API获取图片。将返回图片URL（详情参考[官方文档](https://api.fantasyzone.cc/#/tu) ）。  
参数：   
* __lib__ (`str`) 使用的图库，`pc`为横向动漫壁纸图片 ，`m`为纵向动漫壁纸图片，`mc`为FantasyZone Server截图，`pixiv`为pixiv库图片。传递这些以外的参数会抛出`ValueError`异常。
* __r18__ (`int`) R18状态。`0`为非R18，`1`为R18，`2`为混合，默认为`0`，只能在图库为`pixiv`时生效。传递这些数字以外的参数会抛出`ValueError`异常。
* __not_proxy__ (`bool`) 是否关闭代理模式。默认为`False`。
### 使用实例
```python
>>> from seturequest import get_setu_from_loliconv1 as llc
>>> llc(keyword="镜华", num=2) #获取2张包含“镜华”关键字的涩图
{'code': 0, 'msg': '', 'count': 2, 'data': [{'pid': 75573164, 'p': 0, 'uid': 47999, 'title': 'へんたいふしんしゃさん', 'author': '真崎ケイ／Masaki Kei', 'r18': False, 'width': 1460, 'height': 900, 'tags': ['プリンセスコネクト!Re:Dive', '公主连结Re:Dive', 'キョウカ(プリコネ)', '镜华（公主连结）', 'マイクロビキニ', '极小比基尼', 'おへそ', '肚脐', '照れ顔', 'embarrassed face', '紐水着', 'string swimsuit'], 'url': 'https://i.pixiv.cat/img-original/img/2019/07/06/07/40/57/75573164_p0.jpg'}, {'pid': 78514891, 'p': 0, 'uid': 3342599, 'title': '無題', 'author': '凜凜魚', 'r18': False, 'width': 3354, 'height': 3637, 'tags': ['氷川鏡華', 'Kyouka Hikawa', '剥ぎ取りたいブラ', '让人想脱掉的胸罩', 'エロ衣装', 'H服装', 'キョウカ(プリコネ)', '镜华（公主连结）', 'おへそ', '肚脐', 'プリンセスコネクト!', '公主连结！', '剥ぎ取りたいパンツ', '让人想脱掉的内裤', '性印', 'プリンセスコネクト!Re:Dive', '公主连结Re:Dive'], 'url': 'https://i.pixiv.cat/img-original/img/2020/01/03/13/21/08/78514891_p0.png'}]}
>>> from seturequest import get_setu_from_loliconv2 as llc2
>>> llc2(tag=["萝莉","公主连结Re:Dive"],num=2) #获取两张包含“萝莉”和“公主连结Re:Dive”标签的涩图
{'error': '', 'data': [{'pid': 81886416, 'p': 0, 'uid': 6713521, 'title': '❤孝心变质❤', 'author': '三川MIKAWA', 'r18': '', 'width': 4093, 'height': 2894, 'tags': ['足控', '萝莉', 'loli', '白丝', 'White silk pantyhose', '公主连结', 'Princess Connect', 'プリンセスコネクト!Re:Dive', '公主连结Re:Dive', '可可萝', 'Kokkoro', 'コッコロ', '足指', '脚指'], 'ext': 'jpg', 'uploadDate': 1590536089000, 'urls': {'original': 'https://i.pixiv.cat/img-original/img/2020/05/27/08/34/49/81886416_p0.jpg'}}, {'pid': 74664354, 'p': 0, 'uid': 49100, 'title': '水着コッコロちゃん', 'author': 'ぴざぬこ', 'r18': '', 'width': 1228, 'height': 868, 'tags': ['ロリ', '萝莉', 'プリンセスコネクト!Re:Dive', '公主连结Re:Dive', 'プリコネR', '公主连结', 'コッコロ', '可可萝', '棗こころ', '枣心', '水着', '泳装', 'おしり', '屁股', '女児水着', "little girl's swimsuit"], 'ext': 'jpg', 'uploadDate': 1557500955000, 'urls': {'original': 'https://i.pixiv.cat/img-original/img/2019/05/11/00/09/15/74664354_p0.jpg'}}]}
>>> from seturequest import get_setu_from_fantasyzone as fan
>>> fan()
'https://tva4.sinaimg.cn/large/0072Vf1pgy1foxk43c7brj31hc0u0aw8.jpg'
>>> fan(lib="pixiv") #从pixiv图片库获取图片
'https://pixiv.men/qqWXMnwjLXiD-o-NSoOvSbf38wfLOxSoTZmsBsWQ73QjKlGk2.png'
```