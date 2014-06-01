from django.conf.urls import url

from application.views import *

urlpatterns = [
    url(r'^$', application_main_page),
]
