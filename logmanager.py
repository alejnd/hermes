#!/usr/bin/env python
#  coding: utf-8

import logging

#log levels: DEBUG, INFO, WARN, ERROR, CRITICAL
log = logging.getLogger('ServiceLog')
log.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)-15s [%(levelname)s] %(module)s:%(funcName)s %(message)s')
handler_stream = logging.StreamHandler()
handler_stream.setFormatter(formatter)
handler_stream.setLevel(logging.DEBUG)
log.addHandler(handler_stream)

handler_file = logging.FileHandler('ServiceLog.log')
handler_file.setFormatter(formatter)
log.addHandler(handler_file)
