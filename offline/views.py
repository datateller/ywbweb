from django.shortcuts import render
from django.http import *
from django.utils import http
from datetime import *
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.views.generic import FormView, TemplateView
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance
from django.utils.safestring import SafeString

from .models import *
from .forms import *
from weixin.baidumap import *
import hashlib, time, random
# Create your views here.

def offline_web_view(request, oid):
    try:
        oid = int(oid)
        o = Shop.objects.get(id = oid)
        t = get_template('offline/offline.html')
        c = {}
        c['offline_title'] = o.name
        c['offline_content'] = o.description
        c['offline_address'] = o.address
        picindex = random.randint(0,9)
        c['pic'] = 'http://wjbb.cloudapp.net:8001/pic/'+str(picindex)+'.jpg'
        html = t.render(Context(c))
        return HttpResponse(html)
    except ValueError:
        raise Http404()
    
class ShopFormView(FormView):
    template_name = 'offline/shopform.html'
    form_class = ShopForm
    def get_context_data(self, **kwargs):
        context = super(ShopFormView, self).get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
        address = form.cleaned_data['address']
        baidu_resp = get_baidu_location(address)
        if not baidu_resp['result']:
            baidu_resp = get_baidu_location('百度大厦')
            address = '百度大厦幼儿园'
        longitude = baidu_resp['result']['location']['lng']
        latitude = baidu_resp['result']['location']['lat']
        point = fromstr("POINT(%s %s)" % (longitude, latitude))
        shop = Shop()
        shop.name = form.cleaned_data['name']
        shop.city = form.cleaned_data['city']
        shop.address = form.cleaned_data['address']
        shop.url = form.cleaned_data['url']
        shop.description = form.cleaned_data['description']
        shop.longitude = longitude
        shop.latitude = latitude
        shop.point = point
        shop.save()
        return super(ShopFormView, self).form_valid(form)