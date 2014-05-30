from django.conf.urls import url

from application import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
