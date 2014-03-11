from django.test import TestCase
from .views import *
# Create your tests here.

msg='''<xml>
 <ToUserName><![CDATA[toUser]]></ToUserName>
 <FromUserName><![CDATA[fromUser]]></FromUserName> 
 <CreateTime>1348831860</CreateTime>
 <MsgType><![CDATA[text]]></MsgType>
 <Content><![CDATA[this is a test]]></Content>
 <MsgId>1234567890123456</MsgId>
</xml>'''

def test1():
    print(konwledges_reply(100, 2, weixinmsg_to_map(msg)))
