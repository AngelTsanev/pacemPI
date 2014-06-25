from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import os
from application.webgui import *

@login_required
def application_main_page(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    
    #os.system("raspivid  -ih -t 0 -w 720 -h 405 -fps 25 -b 20000000 -o -")
    #os.system('echo aladin')
    #os.system('''ffmpeg -y \
    #		-loglevel panic \ 
    #		-i - \ 
    #		-c:v copy \
    #		-map 0 \ 
    #		-f ssegment \
    #		-segment_time 1 \
    #		-segment_format mpegts \
    #		-segment_list '$base/stream.m3u8' \				
    #		-segment_list_size 10 \					
    #		-segment_wrap 20 \						
    #		-segment_list_flags +live \					
    #		-segment_list_type m3u8 \					
    #		-segment_list_entry_prefix /cam/segments/ \			
    #		'$base/segments/%03d.ts' ''')

    #os.system("raspivid -t 0 -w 960 -h 540 -fps 25 -b 500000 -vf -o - | ffmpeg -i - -vcodec copy -an -f flv ") # -metadata streamName=myStream tcp://0.0.0.0:6666")
    return HttpResponse(make_html())
   #return render_to_response('application/index.html')
