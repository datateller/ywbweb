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
from .weather import *
from .models import WeixinUser
from .baidumap import *
from .utils import *

reply_null = ''
reply_address_null = '''
对不起，没有获取到您当前的位置，请您回复您宝贝的住址，我们会为您提供更精准的信息～
回复：
生日 20140101
住址 北京市海淀区XXX街XX号
'''
reply0 = '''欢迎来养娃宝瞅一瞅~ 为了获得更精确的知识推送，请在聊天界面告诉我们您家宝宝的生日吧~
回复：
生日 20140101
住址 北京市海淀区XXX街XX号
请注意格式，谢谢~'''
reply1 = '''为了获得更精确的知识推送，请去聊天界面告诉我们您家宝宝的生日和住址吧~
回复：
生日 20140101
住址 北京市海淀区信息路9号
请注意格式，谢谢~'''
reply2 = '''我们已经知道您家宝贝的生日啦~
今后您可以直接点击菜单项 今日知识 获取我们为你量身定制的育儿知识哦~'''
reply3 = '''不好意思哦，我们暂时只能支持0-6岁的宝贝~
更多功能，请下载我们的应用《养娃宝》：'''
reply_location = '''您的位置是 ： %s，更多功能稍后即来~'''
reply_addrok = '''我们已经知道您家宝贝的住址啦~'''
reply_addrerr = '''请填写合法的地址，比如北京市海淀区信息路9号~'''

def weixin_check_view(request):
    echostr = request.GET.get('echostr')
    response = 'weixincheck failed'
    if weixincheck(request):
        print(echostr)
        if echostr:
            response = echostr
    return HttpResponse(response)

def weixin_konwledges_reply(age_by_day, number, msg, weatherinfo):
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
    context['number'] = str(number+1)
    context['create_time'] = str(int(time.time()))
    context["weather_info"] = weatherinfo
    context['temperature'] = weatherinfo['temperature']
    context['wind'] = weatherinfo['wind']
    context['windstrong'] = weatherinfo['windstrong']
    context['detailinfo'] = weatherinfo['detailinfo']
    context['weather_picurl'] = 'http://wjbb.cloudapp.net:8001/pic/'+str(picindexes[0])+'.jpg'
    context['weather_url'] = 'http://wjbb.cloudapp.net/weixin/knowledge/%d/'%(knowls[0].id)
    t = get_template('weixin/knowledges_msg.xml')
    return t.render(Context(context))

def weixin_offline_reply(latitude, longitude, number, msg):
    offlines_nearby = get_offline_nearby(latitude, longitude)
    offlines = None
    count = offlines_nearby.count()
    if(number > count):
        offlines = list(offlines_nearby)
        number = count
    else:
        offlines = random.sample(list(offlines_nearby), number)
    picindexes = random.sample((0,1,2,3,4,5,6,7,8,9), number)
    for i in range(0, number):
        offlines[i].picurl = 'http://wjbb.cloudapp.net:8001/pic/'+str(picindexes[i])+'.jpg'
        offlines[i].url = 'http://wjbb.cloudapp.net/offline/getoffline/%d/'%(offlines[i].id)
    context = {}
    context['offlines'] = offlines
    context['fromUser'] = msg['ToUserName']
    context['toUser'] = msg['FromUserName']
    context['number'] = str(number)
    context['create_time'] = str(int(time.time()))
    t = get_template('weixin/offline_msg.xml')
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
            latitude = weixin_user.latitude
            longitude = weixin_user.longitude
            weatherinfo = ""
            print("in know:long:lat", latitude, longitude)
            if latitude and longitude:
                addr = get_baidu_address(latitude, longitude, False)
                weatherinfo = getweatherinfoconv(addr)
            else:
                weatherinfo = getweatherinfoconv()
            if not baby_birthday:
                return weixin_reply_msg(msg, reply1)
            else:
                return weixin_konwledges_reply(birthday_to_age(baby_birthday.strftime('%Y%m%d')),3,msg, weatherinfo)
        if event_key == 'AROUD_BABY':
            weixin_user = WeixinUser.objects.get(openid=msg['FromUserName'])
            latitude = weixin_user.latitude
            longitude = weixin_user.longitude
            precision = weixin_user.precision
            if latitude and longitude:
                return weixin_offline_reply(latitude, longitude, 2, msg)
#                 baidu_location = convert_baidu_location(latitude, longitude)
#                 if baidu_location and len(baidu_location) == 2:
#                     return weixin_reply_msg(msg, reply_location%(get_baidu_address(baidu_location[0], baidu_location[1])))
#                 else:
#                     return weixin_reply_msg(msg, reply_address_null)
            else:
                return weixin_reply_msg(msg, reply_address_null)
    return msg['Event']

#处理微信请求的view函数
@csrf_exempt
def weixin_dev_view(request):
    try:
        rawstr = smart_str(request.body)
        #print("rawstr:", rawstr)
        msg = weixinmsg_to_map(rawstr)
        reply = ''
        msg_type = msg['MsgType']
        if msg_type == 'text':
            content = msg['Content']
            if content.startswith('生日'):
                birthday_str = content.split(' ')[1]
                age = birthday_to_age(birthday_str)
                if age == 'age_error':
                    reply = reply3
                elif type(age) != int:
                    reply = reply1
                else:
                    weixin_user = WeixinUser.objects.get(openid=msg['FromUserName'])
                    weixin_user.baby_birthday = datetime.strptime(birthday_str, "%Y%m%d")
                    weixin_user.save()
                    reply = reply2
            elif content.startswith('住址'):
                addr = content.split(' ')[1]
                baidu_resp = get_baidu_location(addr)
                if baidu_resp['result']:
                    longitude = float(baidu_resp['result']['location']['lng'])
                    latitude = float(baidu_resp['result']['location']['lat'])
                    weixin_user = WeixinUser.objects.get(openid=msg['FromUserName'])
                    weixin_user.longitude = longitude
                    weixin_user.latitude = latitude
                    weixin_user.precision = 0
                    weixin_user.save()
                    reply = reply_addrok
                else:
                    reply = reply_addrerr
            else:
                reply = reply1
            response = weixin_reply_msg(msg, reply)
            return HttpResponse(response)
        if msg_type == 'event':
            event_out = weixin_event_handle(msg)
            print('event output: %s'%event_out)
            return HttpResponse(event_out)
    except Exception as e:
        print(e)
        return HttpResponse(e)

def weixin_knowledge_view(request, kid):
    try:
        kid = int(kid)
        k = Knowledge.objects.using('wjbbserverdb').get(id = kid)
        #t = get_template('weixin/knowledge.html')
        #c = {}
        #c['knowledge_title'] = k.title
        #c['knowledge_content'] = k.content
        #picindex = random.randint(0,9)
        #c['pic'] = 'http://wjbb.cloudapp.net:8001/pic/'+str(picindex)+'.jpg'
        content = k.content
        html = content
        #if html.find('<img') < 0:
        adaptorstr = '''<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,minimum-scale=1" />'''
        #imagestyle = '''<style type="text/css"> img { width: 100px; height: 241px } </style>'''
        imagestyle = '''<style type="text/css"> div img { display:none } </style>'''
        split1 = html.split('<head>')
        html = ('%s <head> %s %s %s') % (split1[0], adaptorstr, imagestyle, split1[1])
        #print("new html:", html)
        #if html.find('img
        
        imagestart = html.find('<img')
        if imagestart < 0:
        #if True:
           picindex = random.randint(0,9)
           imgstr = '''
<p style=\"text-align: center\">
  <img src=\"%s\" style=\"width: 300px; height: 241px, display:inline\"/>
</p>
''' % ('http://wjbb.cloudapp.net:8001/pic/'+str(picindex)+'.jpg')
           htmlsplit = html.split('<body>')
           html = ('%s <body> %s %s')%(htmlsplit[0], imgstr, htmlsplit[1])

        else:
            srcstart = html.find("src", imagestart)
            srcend = html.find("\"", srcstart + 5)
            imageurl = html[srcstart+5:srcend]
            imgstr = '''
<p style=\"text-align: center\">
  <img src=\"%s\" style=\"width: 300px; height: 241px, display:inline\"/>
</p>
''' % (imageurl)
            htmlsplit = html.split('<body>')
            html = ('%s <body> %s %s')%(htmlsplit[0], imgstr, htmlsplit[1])
            
        #html = t.render(Context(c))
        return HttpResponse(html)
    except ValueError:
        raise Http404()
   

