"""
Definition of urls for VirtAcademy.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm


urlpatterns = patterns('',
    # Examples:
    url(r'^other$', 'app.views.home_other', name='homeOther'),
    
)
