#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmpp

class GtalkAgent:
    def __init__(self,user,passwd):
        self.user   = user
        self.passwd = passwd
        self.client = 'gmail.com'
        self.server = 'talk.google.com'
        
#        self.Connect()
        
    def Connect(self):
        #presence = xmpp.Presence(typ='online', show='chat', status='online')
        #self.conn = xmpp.Client('gmail.com',debug=[])
        self.conn = xmpp.Client(self.client)
        self.conn.connect( server=(self.server,5223) )
        self.conn.auth(self.user, self.passwd, 'Robot')
        self.conn.sendInitPresence()
                                                        
        #presence = xmpp.Presence(typ='online', show='chat', status='online')
        #self.conn.sendInitPresence()
        #self.conn.send(presence)
                                                                                                                                
        
    def Sendmsg(self,to,msg):
        self.Connect()
        for user in to:
            try: self.conn.send(xmpp.Message(user ,msg))
            except:
                print "conn err"
                self.Connect()
                self.conn.send(xmpp.Message(user ,msg ))
    
if __name__ == "__main__":
    gtalkrobot = GtalkAgent('user','password')
    gtalkrobot.Sendmsg (['user@mail.com'],'Hello world!')
       
        
        