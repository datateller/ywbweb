import logging

from django import http
from django import shortcuts
from django.contrib.sessions.models import Session
from django.contrib import messages as django_messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import logout_then_login as django_logout
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.encoding import iri_to_uri

class SubdomainMiddleware(object): 
    def process_request(self, request): 
        domain_parts = request.get_host().split('.') 
        if len(domain_parts) == 3 and domain_parts[0] == 'sj': 
            if not request.path.startswith('/merchant'):
                request.path_info = '/merchant/' 
        print(request.path_info)
