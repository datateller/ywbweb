from django.shortcuts import render
from django.http import *
from django.utils import http
from datetime import *
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context

import xml.etree.ElementTree as ET
import hashlib, time, random
import traceback
import base64, json, random, math
from datetime import datetime

from knowledge.models import Knowledge
from .models import WeixinUser
from .baidumap import *

reply_null = ''
reply_address_null = '''
对不起，没有获取到您当前的位置
'''
reply0 = '''欢迎来养娃宝瞅一瞅~ 为了获得更精确的知识推送，请在聊天界面告诉我们您家宝宝的生日吧~
例如：20140101
请注意格式，谢谢~'''
reply1 = '''为了获得更精确的知识推送，请去聊天界面告诉我们您家宝宝的生日吧~
例如：20140101
请注意格式，谢谢~'''
reply2 = '''我们已经知道您家宝贝的生日啦~
今后您可以直接点击菜单项 今日知识 获取我们为你量身定制的育儿知识哦~'''
reply3 = '''不好意思哦，我们暂时只能支持0-6岁的宝贝~
更多功能，请下载我们的应用《养娃宝》：'''
reply_location = '''您的位置是 ： %s，更多功能稍后即来~'''

def weixin_check_view(request):
    echostr = request.GET.get('echostr')
    response = 'weixincheck failed'
    if weixincheck(request):
        print(echostr)
        if echostr:
            response = echostr
    return HttpResponse(response)

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

def weixin_konwledges_reply(age_by_day, number, msg):
    age = int(age_by_day)
    knowls_all = Knowledge.objects.using('wjbbserverdb').filter(max__gte = age, min__lte = age)
    knowls = None
    count = knowls_all.count()
    if(number >= count):
        knowls = knowls_all
        number = count
    else:
        knowls = random.sample(list(knowls_all), number)
    picindexes = random.sample((0,1,2,3,4,5,6,7,8,9), number)
    for i in range(0, number):
        knowls[i].picurl = 'http://wjbb.cloudapp.net:8001/pic/'+str(picindexes[i])+'.jpg'
        knowls[i].url = 'http://wjbb.cloudapp.net/weixin/knowledge/%d/'%(knowls[i].id)
    context = {}
    context['knowls'] = knowls
    context['fromUser'] = msg['ToUserName']
    context['toUser'] = msg['FromUserName']
    context['number'] = str(number)
    context['create_time'] = str(int(time.time()))
    t = get_template('weixin/knowledges_msg.xml')
    return t.render(Context(context))

def weixin_event_handle(msg):
    if msg['Event'] == 'subscribe':
        new_openid = msg['FromUserName']
        new_user = WeixinUser(openid = new_openid)
        new_user.save()
        return weixin_reply_msg(msg, reply0)
    if msg['Event'] == 'unsubscribe':
        del_openid = msg['FromUserName']
        del_user = WeixinUser.objects.get(openid = del_openid)
        if del_user:
            del_user.delete()
            print('weixin user %s unsubscribe' % del_openid)
        return weixin_reply_msg(msg, reply_null)
    if msg['Event'] == 'LOCATION':
        latitude = msg['Latitude']
        longitude = msg['Longitude']
        precision = msg['Precision']
        weixin_user = WeixinUser.objects.get(openid=msg['FromUserName'])
        weixin_user.latitude = (float)(latitude)
        weixin_user.longitude = (float)(longitude)
        weixin_user.precision = (float)(precision)
        weixin_user.save()
        #return (reply_location%(latitude, longitude, precision))
        print('user  %s location is %s,%s saved in db' % (weixin_user.openid, weixin_user.latitude, weixin_user.longitude))
        return weixin_reply_msg(msg, reply_null)
    if msg['Event'] == 'CLICK':
        event_key = msg['EventKey']
        if event_key == 'TODAY_KNOWLEDGE':
            weixin_user = WeixinUser.objects.get(openid=msg['FromUserName'])
            baby_birthday = weixin_user.baby_birthday
            if not baby_birthday:
                return weixin_reply_msg(msg, reply1)
            else:
                return weixin_konwledges_reply(birthday_to_age(baby_birthday.strftime('%Y%m%d')),3,msg)
        if event_key == 'AROUD_BABY':
            weixin_user = WeixinUser.objects.get(openid=msg['FromUserName'])
            latitude = weixin_user.latitude
            longitude = weixin_user.longitude
            precision = weixin_user.precision
            if latitude and longitude and precision:
                baidu_location = convert_baidu_location(latitude, longitude)
                if baidu_location and len(baidu_location) == 2:
                    return weixin_reply_msg(msg, reply_location%(get_baidu_address(baidu_location[0], baidu_location[1])))
                else:
                    return weixin_reply_msg(msg, reply_address_null)
            else:
                return weixin_reply_msg(msg, reply_address_null)
    return msg['Event']

#处理微信请求的view函数
@csrf_exempt
def weixin_dev_view(request):
    try:
        rawstr = smart_str(request.body)
        msg = weixinmsg_to_map(rawstr)
        reply = ''
        msg_type = msg['MsgType']
        if msg_type == 'text':
            age = birthday_to_age(msg['Content'])
            if age == 'age_error':
                reply = reply3
            elif type(age) != int:
                reply = reply1
            else:
                weixin_user = WeixinUser.objects.get(openid=msg['FromUserName'])
                weixin_user.baby_birthday = datetime.strptime(msg['Content'], "%Y%m%d")
                weixin_user.save()
                reply = reply2
            response = weixin_reply_msg(msg, reply)
            return HttpResponse(response)
        if msg_type == 'event':
            event_out = weixin_event_handle(msg)
            print('event output: %s'%event_out)
            return HttpResponse(event_out)
    except Exception as e:
        print(e)
        return HttpResponse(e)

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

def weixin_knowledge_view(request, kid):
    try:
        kid = int(kid)
        k = Knowledge.objects.using('wjbbserverdb').get(id = kid)
        t = get_template('weixin/knowledge.html')
        c = {}
        c['knowledge_title'] = k.title
        c['knowledge_content'] = k.content
        picindex = random.randint(0,9)
        c['pic'] = 'http://wjbb.cloudapp.net:8001/pic/'+str(picindex)+'.jpg'
        html = t.render(Context(c))
        return HttpResponse(html)
    except ValueError:
        raise Http404()
   

