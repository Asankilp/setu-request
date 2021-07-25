# setu-request
涩图的请求与下载。（服务由[Lolicon API](http://api.lolicon.app)提供）
## QQ机器人  
`setu_qqbot.py`可通过uvicorn运行服务器，通过[go-cqhttp](http://github.com/Mrs4s/go-cqhttp)或其他遵循[OneBot 标准](https://github.com/howmanybots/onebot)的机器人库来对QQ机器人提供支持。  
使用[NoneBot](https://github.com/nonebot/nonebot)框架的机器人位于[该目录](nonebot)下。运行`run.py`并通过[go-cqhttp](http://github.com/Mrs4s/go-cqhttp)或其他遵循[OneBot 标准](https://github.com/howmanybots/onebot)的机器人库来对QQ机器人提供支持。
## web 版本
web 版本可通过运行`server/run.py`开启简易服务器，并通过指定的端口在浏览器访问。
