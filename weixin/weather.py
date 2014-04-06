import requests
from django.http import HttpResponse
from django.utils.translation import ugettext as _
import json
import os

def getcontent(loccode="101010100"):
    base = "http://www.weather.com.cn/data/sk/"
#requests.get("http://m.weather.com.cn/data/101110102.html")
    urln = base+loccode
    resp = requests.get(base+loccode+".html")
    content = resp.json()
    #print(content)
    return content['weatherinfo']

def getweatherinfo1(loccode="101010100"):
    wtinfo = getcontent(loccode)
    response_data = {}
    response_data['city'] = wtinfo['city']
    #print(wtinfo['city'])
    response_data['date'] = wtinfo['date_y']
    response_data['temperature'] = wtinfo['temp1']
    response_data['weather'] = wtinfo['weather1']
    response_data['info'] = wtinfo['index']
    response_data['detailinfo'] = wtinfo['index_d']
    #return HttpResponse(json.dumps(response_data), content_type = "application/json; charset=utf-8")
    #return HttpResponse(json.dumps(response_data, ensure_ascii=False).encode('utf-8'), content_type = "application/json; charset=utf-8")
    #return HttpResponse(wtinfo, content_type = "text/plain")
    #return json.dumps(response_data, ensure_ascii=False).encode('utf-8')
    return response_data

def gethint(tempstr):
    temp = int(tempstr)
    if temp <= 0:
        return "天气寒冷，穿羽绒服保暖"
    if temp >= 0 and temp < 10:
        return "温度较低，穿毛衣保暖"
    if temp >= 10 and temp < 25:
        return "温度适宜，穿衬衣或羊毛衫"
    if temp >= 25:
        return "温度较高，穿短袖裙子，避免中暑"

def getweatherinfo(loccode="101010100"):
    wtinfo = getcontent(loccode)
    response_data = {}
    response_data['city'] = wtinfo['city']
    #print(wtinfo['city'])
    response_data['temperature'] = wtinfo['temp']
    response_data['wind'] = wtinfo['WD']
    response_data['windstrong'] = wtinfo['WS']
    response_data['detailinfo'] = gethint(wtinfo['temp'])
    #return HttpResponse(json.dumps(response_data), content_type = "application/json; charset=utf-8")
    #return HttpResponse(json.dumps(response_data, ensure_ascii=False).encode('utf-8'), content_type = "application/json; charset=utf-8")
    #return HttpResponse(wtinfo, content_type = "text/plain")
    #return json.dumps(response_data, ensure_ascii=False).encode('utf-8')
    return response_data

def getweatherinfoconv(locstr=""):
   curpath = os.getcwd()
   loccode = "101010100"
   with open(curpath+"/weixin/locconv.txt") as f:
     for line in f:
       sline = line.split(" ")
       place = sline[0]
       #print place
       #if locstr == unicode(place.decode('utf-8')):
       #if locstr == str(place, 'utf-8'):
       #if locstr == place:
       if locstr.startswith(place):
         loccode = sline[1].strip()
         #print("match:", loccode)
         break
   return getweatherinfo(loccode)
    

