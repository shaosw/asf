#!/bin/env python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import tornado.gen
import os
import xml.etree.ElementTree as ET
import datetime
import time
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import requests
from WXBizMsgCrypt import WXBizMsgCrypt
#####以下3行需要填入自己的信息
sToken = ""
sEncodingAESKey = ""
sCorpID = ""
################

class main(tornado.web.RequestHandler):
    def checksig(self,sToken,sEncodingAESKey,sCorpID):
        wxcpt=WXBizMsgCrypt(sToken,sEncodingAESKey,sCorpID)
        return wxcpt
    def get(self):
        sVerifyTimeStamp=self.get_argument('timestamp')
        sVerifyMsgSig=self.get_argument('msg_signature')
        sVerifyNonce=self.get_argument('nonce')
        sVerifyEchoStr=self.get_argument('echostr')
        wxcpt=self.checksig(sToken,sEncodingAESKey,sCorpID)
        ret,sEchoStr=wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp,sVerifyNonce,sVerifyEchoStr)
        if(ret!=0):
            print "ERR: VerifyURL ret: " + str(ret)
            sys.exit(1)
        self.write(sEchoStr)
    def post(self):
        wxcpt=self.checksig(sToken,sEncodingAESKey,sCorpID)
        sReqTimeStamp=self.get_argument('timestamp')
        sReqMsgSig=self.get_argument('msg_signature')
        sReqNonce=self.get_argument('nonce')
        sReqData=self.request.body
        ret,sMsg=wxcpt.DecryptMsg( sReqData, sReqMsgSig, sReqTimeStamp, sReqNonce)
        if( ret!=0 ):
            print "ERR: DecryptMsg ret: " + str(ret)
            sys.exit(1)
        data = ET.fromstring(sMsg)
        tousername = data.find('ToUserName').text
        fromusername = data.find('FromUserName').text
        msgtype = data.find('MsgType').text
        if msgtype=='text':
            content =data.find("Content").text
            response=self.get_asf(content)
            sRespData = """<xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[%s]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>""" % (fromusername,tousername,str(int(time.time())),'text',response)
        ret,sEncryptMsg=wxcpt.EncryptMsg(sRespData, sReqNonce, sReqTimeStamp)
        if( ret!=0 ):
            print "ERR: EncryptMsg ret: " + str(ret)
            sys.exit(1)
        self.write(sEncryptMsg)
    def get_asf(self,msg):
        ipcUrl = 'http://127.0.0.1:1242/IPC'
        try:
            r = requests.get(ipcUrl, params={'command':msg})
            return r.text    
        except:
            return
class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
                 (r'/wx', main)
]
        settings = {
        "debug":True,
        "autoescape":None,
    }
        tornado.web.Application.__init__(self, handlers, **settings)
if __name__ == '__main__':
#自定义端口 ,python filename.py 运行
    port=80
    app=Application()
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app,xheaders=True)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
