import picamera
import smtplib
import os
import glob

from email.mime.text      import MIMEText
from email.mime.base      import MIMEBase
from email.mime.multipart import MIMEMultipart
from email                import encoders
from time                 import sleep


def next_filename(DIR='/home/haolam05/Desktop/475/images', FILE_PREFIX='image', EXTENSION='jpg'):
    # create a folder for images if not yet created
    if not os.path.exists(DIR):
        os.makedirs(DIR)

    # Find the largest ID of existing images, start new images after this ID value
    # 1. Return a list path names that match pathname specification and sort them
    pathname_spec = os.path.join(DIR, FILE_PREFIX + '[0-9][0-9][0-9].' + EXTENSION)
    paths         = glob.glob(pathname_spec)
    files         = sorted(paths)

    # 2. Grab the count from the last filename,
    #    starts from right, take string from idx place 7 to 4 to get the count
    count = 0;
    if len(files) > 0:
        extension_len = len(EXTENSION)
        count         = int(files[-1][-extension_len-4:-extension_len-1])+1  # 4: "000."

    # return next filename
    return os.path.join(DIR, FILE_PREFIX + '%03d.{}'.format(EXTENSION) % count)

def send(default_msg    = "Image of the Suspicious Intruder!",
         receiver_email = "quanv1024@gmail.com"):

    # Capture photo from PiCamera amd save to filename
    filename = next_filename()
    capture_pic(filename)
    #filename = '/home/haolam05/Desktop/475/images/image000.jpg'
    #filename = next_filename('/home/haolam05/Desktop/475/videos', 'video', 'h264')
    #record(filename)

    # Credentials
    sender   = "tuonghao2001@gmail.com"
    password = "nvztoaxnqppnenyp"
    receiver = receiver_email

    # Messages multipart
    body           = 'Picture is Attached.'
    attachment     = open(filename, 'rb')
    msg            = MIMEMultipart()
    msg['From']    = sender
    msg['To']      = receiver
    msg['Subject'] = default_msg
    msg.attach(MIMEText(body, 'plain'))
    part           = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename= %s' % filename)
    msg.attach(part)
    text           = msg.as_string()

    # Sending mail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, text)
    server.quit()

def capture_pic(filename):
    with picamera.PiCamera() as camera:
        camera.capture(filename)

def record(filename, seconds=5):
    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.start_recording(filename)
        sleep(seconds)
        camera.stop_recording()
        camera.stop_preview()