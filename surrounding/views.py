from django.shortcuts import render
# Create your views here.
from django.views.generic import FormView, TemplateView
from django.contrib.gis.geos import Point, fromstr
from django.contrib.gis.measure import D # alias for Distance
from django.utils.safestring import SafeString
from django.http import *
from .forms import *
from .models import *
# Create your views here.
import json

class UserFormView(FormView):
    template_name = 'surrounding/userform.html'
    form_class = UserForm
    def get_context_data(self, **kwargs):
        context = super(UserFormView, self).get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
        longitude = form.cleaned_data['longitude']
        latitude = form.cleaned_data['latitude']
        point = fromstr("POINT(%s %s)" % (longitude, latitude))
        print(point.x)
        newuser = EndUserLocation(point = point)
        newuser.save()
        return super(UserFormView, self).form_valid(form)
    

class MerchantLocationFormView(FormView):
    template_name = 'surrounding/merchantform.html'
    form_class = MerchantLocationForm
    def get_context_data(self, **kwargs):
        context = super(MerchantLocationFormView, self).get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
        longitude = form.cleaned_data['longitude']
        latitude = form.cleaned_data['latitude']
        point = fromstr("POINT(%s %s)" % (longitude, latitude))
        newmer = MerchantLocation(point = point)
        newmer.save()
        return super(MerchantLocationFormView, self).form_valid(form)
    
class MapView(TemplateView):
    template_name = 'map.html'
    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        mername = self.request.GET['mername']
        distance = self.request.GET['distance']
        merp = MerchantLocation.objects.get(name = mername).point
        userpoints = []
        nearbyusers = EndUserLocation.objects.filter(point__distance_lt=(merp, D(km=int(distance)/1000)))
        for user in nearbyusers:
            x = user.point.x
            y = user.point.y
            userpoints.append({'x':x,'y':y})
            print(user.point)
        context['merx']=merp.x
        context['mery']=merp.y
        context['distance']=distance
        context['userpoints']=SafeString(json.dumps(userpoints))
        print(mername)
        return context

def surrounding_view(request):
    longitude = request.GET['longitude']
    latitude = request.GET['latitude']
    distance = request.GET['distance']
    merp = point = fromstr("POINT(%s %s)" % (longitude, latitude))
    userpoints = []
    nearbyusers = EndUserLocation.objects.filter(point__distance_lt=(merp, D(km=int(distance)/1000)))
    for user in nearbyusers:
        x = user.point.x
        y = user.point.y
        userpoints.append({'x':x,'y':y})
        print(user.point)
#     context['merx']=merp.x
#     context['mery']=merp.y
#     context['distance']=distance
#     context['userpoints']=SafeString(json.dumps(userpoints))
    return HttpResponse(SafeString(json.dumps(userpoints)))