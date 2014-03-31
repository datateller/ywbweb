from django.utils.encoding import smart_str
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance

import xml.etree.ElementTree as ET
import hashlib, time, random
import traceback
import base64, json, random, math
from datetime import datetime

from offline.models import *


def get_offline_nearby(latitude, longitude, number):
    distance = 5000
    point = fromstr("POINT(%s %s)" % (longitude, latitude))
    nearbys = Shop.objects.filter(point__distance_lt=(point, D(km=int(distance)/1000)))
    return nearbys

def weixinmsg_to_map(rawstr):
    msg = {}
    rootelem = ET.fromstring(rawstr)
    if rootelem.tag == 'xml':
        for child in rootelem:
            msg[child.tag] = smart_str(child.text)
    return msg

def weixin_reply_msg(msg, reply_content):
    xml_tpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    reply_msg = xml_tpl % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'text',reply_content)
    return reply_msg


#检查请求是否来源于微信
def weixincheck(request):
    signature = request.GET.get('signature')
    if not signature:
        return False
    timestamp = request.GET.get('timestamp')
    if not timestamp:
        return False
    nonce = request.GET.get('nonce')
    if not nonce:
        return False
    #if not isinstance(timestamp, (str, unicode)):
    timestamp = str(timestamp)
    token = '1234abcd'
    args = [token, timestamp, nonce]
    args.sort()
    my_signature = hashlib.sha1((''.join(args)).encode(encoding='utf-8')).hexdigest()
    if my_signature == signature:
        return True
    else:
        return False

def birthday_to_age(birthday_str):
    today = datetime.now()
    try:
        d = datetime.strptime(birthday_str, "%Y%m%d")
        days = (today - d).days
        print('baby age by day is %d' % days)
        if days//365 not in (0,1,2,3,4,5,6):
            return 'age_error'
        else:
            return days
    except Exception as e:
        return e