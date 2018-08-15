# asf_weixin
https://steamcn.com/t303436-1-1
教程开始：
1 需要企业微信，个人也能注册 
2 一台服务器，部署asf，运行脚本


具体步骤：
1  部署linux 的asf3.0，具体论坛都有，使用./ArchiSteamFarm --server  开启IPC

2 打开http://work.weixin.qq.com/ ，右上选择企业注册，选择组织，选择没有组织机构代码证，继续注册，绑定自己的微信
  
注册完毕后，登入，点击我的企业
记下CorpID
创建应用
  


  点击使用api接受消息，填入服务器URL/wx
点击  随机获取 ，记下Token和EncodingAESKey
然后暂停


3  把脚本上传到linux机器上，3个文件必须在同一个目录
修改脚本内容
vim main.py
复制代码
修改
sToken = ""
sEncodingAESKey = ""
sCorpID = ""

:wq  #保存退出
#安装库
pip install pycrypto  requests  tornado
#运行脚本
python main.py
复制代码



4 
在第二步的页面点击保存
认证成功后就可以，通过发送微信消息转发到asf ipc上了

5 然后在企业微信后台，邀请自己，扫码关注后，在微信就能看到聊天了
