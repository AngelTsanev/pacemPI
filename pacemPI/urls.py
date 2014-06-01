from django.conf.urls import include, url
from pacemPI.views import *
from django.contrib import * #admin

urlpatterns = [
    url(r'^application/', include('application.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', main_page),

    # Login / logout.
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),

    # Serve static content.
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'static'}),
]
