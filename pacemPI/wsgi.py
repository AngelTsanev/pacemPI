"""
WSGI config for pacemPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pacemPI.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


def on_startup():
   os.system("mkdir /tmp/stream 2> /dev/null")
   os.system("raspistill -w 640 -h 480 -q 20 -o /tmp/stream/pic.jpg -tl 50 -t 9999999 2> /dev/null &")

   os.system("""sudo cp /home/pi/mjpg-streamer-code-182/mjpg-streamer/output_http.so /home/pi/mjpg-streamer-code-182/mjpg-streamer/input_file.so /usr/local/lib/ 2>/dev/null""")

   os.system("""LD_LIBRARY_PATH=/usr/local/lib mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /usr/local/www" &""")

on_startup()


