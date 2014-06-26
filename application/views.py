from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os
from application.draw_temperature import *

@login_required
def application_main_page(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    #os.system("raspistill -w 640 -h 480 -n -q 15 -o /tmp/stream/pic.jpg -tl 100 -t 9999999 2> /dev/null")
    return render_to_response('application/index.html')

def application_temperature(request, interval):
    return HttpResponse(make_html(interval))
