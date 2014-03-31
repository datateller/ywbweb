import requests
from django.http import HttpResponse
from django.utils.translation import ugettext as _
import json
import os

def getcontent(loccode="101010100"):
    base = "http://m.weather.com.cn/data/"
#requests.get("http://m.weather.com.cn/data/101110102.html")
    urln = base+loccode
    #print("urln:", urln)
    resp = requests.get(base+loccode+".html")
    content = resp.json()
    #print(content)
    return content['weatherinfo']

def getweatherinfo(loccode="101010100"):
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

def getweatherinfoconv(locstr=""):
   #print("locstr:", locstr)
   curpath = os.getcwd()
   print("weixin curpath:", curpath)
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
    

