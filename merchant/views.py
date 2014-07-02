from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, ProcessFormView
from django.contrib.auth.models import User 
from django.contrib import auth
from django import forms
from .forms import *
from .models import *
from django.http import *
from django.shortcuts import render_to_response
from  django.template import RequestContext
from registration.backends.default.views import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import connections
from django.contrib.gis.geos import Point, fromstr
# Create your views here.


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
            merchant = Merchant.objects.filter(user__username = username)[0]
            rcontext = RequestContext(request, locals())
            return render_to_response(MerchantHomeView.template_name, rcontext)
        else:
            rcontext = RequestContext(request, locals())
            return render_to_response(MerchantMainPageView.template_name, rcontext)
    else:
        return HttpResponseRedirect("/merchant/")


def logout_view(request):
    user = request.user
    if user is not None:
        auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/merchant/")


class RegisterView(RegistrationView):
    template_name = 'merchant/register.html'
    form_class = RegisterForm
    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['register_form'] = RegisterForm()
        return context

    def form_valid_old(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        ###process register form
        if self.request.method == 'POST':
            form_reg = RegisterForm(self.request.POST)
            if form_reg.is_valid():
                username = form_reg.cleaned_data['email']
                user = User.objects.create_user(username = username,
                                            password = form_reg.cleaned_data['password'],
                                            email = form_reg.cleaned_data['email'])
                merchant = Merchant(user = user)
                merchant.city = form_reg.cleaned_data['city']
                merchant.address = form_reg.cleaned_data['address']
                print("longitude is :" + form_reg.cleaned_data['longitude'])
                merchant.longitude = float(form_reg.cleaned_data['longitude'])
                merchant.latitude = form_reg.cleaned_data['latitude']
                merchant.description = form_reg.cleaned_data['description']
                merchant.name = form_reg.cleaned_data['name']
                merchant.point = fromstr("POINT(%s %s)" % (merchant.logitude, merchant.latitude))
                #user.save()
                print("###merchant name:", merchant.name)
                print("####merchange save")
                merchant.save()
            else:
                print("###error: not post?")
                print("###qiguai")
        return super(RegisterView, self).form_valid(form)
    def form_valid(self, form_reg):
        username = form_reg.cleaned_data['email']                                
        user = User.objects.create_user(username = username,                     
        password = form_reg.cleaned_data['password'],
        email = form_reg.cleaned_data['email'])
        merchant = Merchant(user = user)
        merchant.city = form_reg.cleaned_data['city']
        merchant.address = form_reg.cleaned_data['address']
        print("###form valid longitude is :" + form_reg.cleaned_data['longitude'])             
        merchant.longitude = float(form_reg.cleaned_data['longitude'])
        merchant.latitude = form_reg.cleaned_data['latitude']
        merchant.description = form_reg.cleaned_data['description']
        merchant.name = form_reg.cleaned_data['name']
        print("###merchant name:", merchant.name)
        print("####merchange save")
        merchant.save()
        return super(RegisterView, self).form_valid(form_reg)


class MerchantMainPageView(TemplateView):
    template_name = 'merchant/mainpage.html'
    def get_context_data(self, **kwargs):
        context = super(MerchantMainPageView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context


class MerchantHomeView(TemplateView):
    template_name = 'merchant/merchant_home.html'
    
    def get_context_data(self, **kwargs):
        context = super(MerchantHomeView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
       
        context['merchant'] = merchant = Merchant.objects.filter(user__username = self.request.user.username)[0]
        userpoints = []
        merp = fromstr("POINT(%s %s)" % (merchant.longitude, merchant.latitude))
        nearbybabys = Baby.objects.using("ywbdb").filter(homepoint__distance_lt=(merp, D(km=int(5000)/1000)))
        for baby in nearbybabys:
            print("###baby x:",baby.homepoint.x,"###baby y:",baby.homepoint.y)
            userpoints.append({'x':baby.homepoint.x, 'y':baby.homepoint.y})

        context['userpoints'] = userpoints
        
        return context

        

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MerchantHomeView, self).dispatch(*args, **kwargs)


class CommercialListView(TemplateView):
    template_name = 'merchant/commercial_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(CommercialListView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        user = self.request.user
        merchant = user.merchant
        clist = []
        clist = Commercial.objects.filter(merchant = merchant)
        context['commercial_list'] = clist
        context['merchant'] = Merchant.objects.filter(user__username = self.request.user.username)[0]
        return context
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CommercialListView, self).dispatch(*args, **kwargs)
    
    
class CommercialPostView(FormView):
    form_class = PostCommercialForm
    template_name = 'merchant/commercial_post.html'
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CommercialPostView, self).dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(CommercialPostView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['post_form'] = PostCommercialForm()
        context['merchant'] = Merchant.objects.filter(user__username = self.request.user.username)[0]
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        ###process register form
        if self.request.method == 'POST':
            form_post = PostCommercialForm(self.request.POST, self.request.FILES)
            if form_post.is_valid():
                temp = form_post.save(commit=False)
                temp.merchant = self.request.user.merchant
                if self.request.FILES:
                    temp.photo = self.request.FILES['photo']
                temp.save()
            else:
                print(form_post.errors)
                print("form_post not valid")
        return super(CommercialPostView, self).form_valid(form)

def about(request):
    return render(request, "merchant/about.html")

from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km 


class PromotionView(TemplateView):
    template_name = 'merchant/promotion_effect.html'
    
    def get_context_data(self, **kwargs):
        context = super(PromotionView, self).get_context_data(**kwargs)
        commercialid = kwargs["commercial_id"]

        context['merchant'] = merchant = Merchant.objects.filter(user__username = self.request.user.username)[0]
        userpoints = []
        merp = fromstr("POINT(%s %s)" % (merchant.longitude, merchant.latitude))
        nearbybabys = Baby.objects.using("ywbdb").filter(homepoint__distance_lt=(merp, D(km=int(5000)/1000)))
        seenhistory = CommercialHistory.objects.filter(commercial_id=commercialid)
        seenbabys = [Baby.objects.using("ywbdb").get(id=history.baby_id) for history in seenhistory]
        
        for baby in nearbybabys:
            print("###babyid:", baby.id)
            print("###baby x:",baby.homepoint.x,"###baby y:",baby.homepoint.y)
            babydistance = min(int(haversine(merchant.longitude, merchant.latitude, baby.homepoint.x, baby.homepoint.y)*1000), 5000)
            haveseen = False
            if baby in seenbabys:
                haveseen = True
            userpoints.append({'x':baby.homepoint.x, 'y':baby.homepoint.y, 'distance':babydistance, 'haveseen':haveseen})
        context['userpoints'] = userpoints
        return context
