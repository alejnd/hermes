#!/usr/bin/env python
#  coding: utf-8

import json
import urllib2
 
data = {'msg':'debug testing','log_level':'DEBUG'}
data = json.dumps(data)
 
url = "http://localhost:5000/twitter/notify"
 
req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
 
f = urllib2.urlopen(req)
response = f.read()
print response
f.close()
