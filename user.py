#!/usr/bin/env python
#  coding: utf-8
from ConfigParser import *

class User:
    def __init__(self, config):
        self.username = config.get('user','username')
        self.password = config.get('user','password')
        self.id       = config.get('user','id')
        
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
        
if __name__ == '__main__':
    config = SafeConfigParser()
    config.read('hermes.cfg')
    User =User(config)
    print User.username, User.id
        
