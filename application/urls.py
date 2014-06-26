from django.conf.urls import url

from application.views import *

urlpatterns = [
    url(r'^temperature/(?P<interval>[0-9]+)/$', application_temperature),
    url(r'^$', application_main_page),
]
