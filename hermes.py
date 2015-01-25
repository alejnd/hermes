#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from xmlrpclib import Server

from gtalklib import *
from mailib import *
from twitterlib import *
from ConfigParser import *

class Hermes:
    def __init__(self, config):
        
        self.config = config
        self.initgtalk()
        self.initmail()
        self.inittwiter()
        
    #def readconfig(self):
    #    self.config = SafeConfigParser()
    #    self.config.read('hermes.cfg')
                                
    def initgtalk (self):
        user   = self.config.get('gtalk','user')
        passwd = self.config.get('gtalk','passwd')
        self.gtalkrobot = GtalkAgent(user, passwd)
    
    def initmail (self):
        user   = self.config.get('mail','user')
        passwd = self.config.get('mail','passwd')
        self.mailrobot =  MailAgent(user, passwd)
    
    def inittwiter (self):
        
        con_key    = self.config.get('twitter','consumer_key')
        con_secret = self.config.get('twitter','consumer_secret')
        acc_token  = self.config.get('twitter','access_token')
        acc_secret = self.config.get('twitter','access_secret')
        self.twitterrobot = TwitterAgent(con_key, con_secret, acc_token, acc_secret)

        
    def saludo (self, nombre):
        return "Hola " + str(nombre)
    
    def notify (self, msg, to=None, subject='',via='gtalk'):
        
        if   via == 'gtalk':   self.gtalkrobot.Sendmsg(to,msg)
        elif via == 'email':   self.mailrobot.Sendmsg(to,msg,subject)
        elif via == 'twitter': self.twitterrobot.Sendmsg(msg) 
        else: print 'via not found'

if __name__ == "__main__":
    config = SafeConfigParser()
    config.read('hermes.cfg')
    notifyAgent = Hermes(config)
    notifyAgent.notify('hello world','mail@mail.com')
    notifyAgent.notify('moar test', via='twitter') 

        
