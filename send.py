import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def SendMail(ImgFileName):
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'ALERT'
    msg['From'] = 'serversoyuz@gmail.com'
    msg['To'] = 'spalf0@gmail.com'

    text = MIMEText("Intruder.")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login(msg['From'], 'password')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
