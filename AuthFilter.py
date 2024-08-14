# -*- coding: utf-8 -*-

import tornado.web
import hashlib

class AuthFilter(object):
    def __init__(self):
        pass

    def __del__(self):
        pass
    
    def doFilter(self, requestHandler):
        '''
        #FIXME: super header! to do!
        
        i = requestHandler.request.headers.get(r'X-I')
        s = requestHandler.request.headers.get(r'X-S')
        if not i or not s:
            return False
        
        i = requestHandler.get_cookie('I')
        s = requestHandler.get_cookie('S')
        if not i or not s:
            return False
        
        m = hashlib.md5()
        m.update("A7Bx9cXVGIzY18LJy7GaZbeYAGeOfPNDqCPLVUtvJfQPXbCCLWA8ac")
        m.update("_" + i)
        sign = m.hexdigest()
        
        if s == sign:
            return True
        else:
            return False
        '''
        return True
        