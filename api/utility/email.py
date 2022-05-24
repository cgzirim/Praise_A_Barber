import os
import smtplib


def send_mail(receiver, subject, body):
    gmail_user = os.environ.get('MAIL_ADDRESS')
    gmail_pwd = os.environ.get('MAIL_PASSWORD')
    message = "\From: %s\nTo: %s\nSubject: %s\n\n%s" % (gmail_user, receiver, subject, body)
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    smtpserver.sendmail(gmail_user, receiver, message)
    smtpserver.close()
