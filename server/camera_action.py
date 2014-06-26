import smtplib
import picamera
import time
import os
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  

FROM = 'pacempi2@gmail.com'
TO   = 'angeltzanev@gmail.com'
SMTP_SERVER_PORT = 'smtp.gmail.com:587'
USERNAME = 'pacempi2@gmail.com'
PASSWORD = 'konopida'
IMAGE_FOLDER = '/home/pi/pacemPI/images/'


def send_mail(filename):
    message = MIMEMultipart()
    message['From'] = FROM
    message['To'] = TO
    message['Subject'] = '****ALERT****'

    text = MIMEText("You have intruder in your room!")
    message.attach(text)

    image = MIMEImage(open(IMAGE_FOLDER + filename, 'rb').read(), _subtype="jpg")
    image.add_header('Content-Disposition', 'attachment; filename="%s"'
                   % filename)
    message.attach(image)

    session = smtplib.SMTP(SMTP_SERVER_PORT)
    session.starttls()
    session.login(USERNAME, PASSWORD)
    session.sendmail(FROM, TO, message.as_string())
    session.quit()

    #server = smtplib.SMTP('smtp.gmail.com:587')
    #server.starttls()
    #server.login(username,password)
    #server.sendmail('archa40@gmail.com', 'angeltzanev@gmail.com', message)
    #server.quit()

def take_picture(filename):
    os.system("killall raspistill")
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(0.5)
        camera.capture(IMAGE_FOLDER + filename)
        camera.stop_preview()
        os.system("raspistill -w 640 -h 480 -q 20 -o /tmp/stream/pic.jpg -tl 50 -t 9999999 2> /dev/null &")

def alert():
    filename = time.strftime("%d%m%H%M%S") + '.jpg'
    take_picture(filename)
    send_mail(filename)

#alert()
