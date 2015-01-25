#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy

class TwitterAgent():
    def __init__(self,con_key, con_secret, acc_key, acc_secret):
        self.consumer_key        = con_key
        self.consumer_secret     = con_secret
        self.access_token_key    = acc_key
        self.access_token_secret = acc_secret
    
    def getauth(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token_key, self.access_token_secret)
        t = tweepy.API(auth)
        return t
    
    def Sendmsg(self, msg):
        t = self.getauth()
        status = t.update_status(msg)
        
if __name__ == "__main__":
    pass