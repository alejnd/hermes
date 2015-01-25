#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.MIMEText import MIMEText

class MailAgent:
    def __init__(self,user,passwd):
        self.host   = 'smtp.gmail.com'
        self.user   = user
        self.passwd = passwd
        
            
    def Connect(self):
        self.conn = smtplib.SMTP(self.host)
        self.conn.ehlo()
        self.conn.starttls()
        self.conn.login(self.user, self.passwd)
    
    def Disconnect(self):
        self.conn.close()
        
    def Sendmsg(self,to,msg,subject):
        self.Connect()
        
        mail = MIMEText(msg)
        mail['From'] = self.user
        if type(to) == str: mail['To'] = to
        else: mail['To'] = to[0]
        mail['Subject'] = subject
        self.conn.sendmail(mail['From'],to,mail.as_string())
        self.Disconnect()
    
if __name__ == "__main__":
    mailrobot = MailAgent('user@mail.com','passs') 
    mailrobot.Connect()
    mailrobot.Sendmsg(['user1@mail.com','user2@mail.com'],'testing mailrobot','mremirobot2')
    mailrobot.Disconnect()
    