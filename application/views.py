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
    
    #os.system("raspivid  -ih -t 0 -w 720 -h 405 -fps 25 -b 20000000 -o -")
    #os.system('echo aladin')
    return render_to_response('application/index.html')

def application_temperature(request, interval):
    return HttpResponse(make_html(interval))
