# -*- coding: utf-8 -*-

import abc
import tornado.web
import os
import hashlib
import random
import json
import sys
import stat
import time
#from pgmagick import Image
import settings
from AuthFilter import AuthFilter

class FastImageHandler(tornado.web.RequestHandler):
    def initialize(self, bak_path = None, path = None, auth = None):
        if not path :
            self.open_flag = False
            self.file_dir = None
        else :
            self.open_flag = True
            self.file_dir = os.path.join(path, "image")
            
        if bak_path:
            self.bak_path = os.path.join(bak_path, "image")
        else:
            self.bak_path = None
            
        if auth:
            self.auth_filter = auth
        else :
            self.auth_filter = None

        self.return_url_prefix = "http://p" + str(settings.SHARD_ID)
        pass
    
    def post(self, group='common'):
        self.write("upload_fast_image: " + group)
        pass

    def get(self, group='common'):
        ret = {
            "error" : 0, 
            "message" : [] 
        }
        if self.open_flag:
            if self.auth_filter and self.auth_filter.doFilter(self):
                name_list = self.get_argument("names")

                if name_list :
                    name_list = name_list.split(',')
                    for name in name_list:
                        rawname = name.encode('UTF-8')
                        [front, end] = rawname.rsplit('.', 1)
                        
                        if True or end in [] :
                            m = hashlib.md5()
                            m.update(front + str(int(time.time())) + str(random.random()))
                            m.digest()
                            m = m.hexdigest()
                            [first_d, second_d, third_d, name] = [m[0:2], m[2:4], m[4:6], m]
            
                            rename =  name + '.' + end

                            if settings.ENV == 'product':
                                ret["message"].append(self.return_url_prefix  + settings.DOMAIN  + "/image/" + group + "/" + rename)
                            elif settings.ENV == 'idc_test':
                                ret["message"].append('http://' + settings.IDC_TEST_IP + "/image/" + group + "/" + rename)
                            elif settings.ENV == 'test':
                                ret["message"].append('http://' + settings.TEST_IP + "/image/" + group + "/" + rename)
                            else:
                                ret["message"].append('The env is error!')
                        else:
                            ret["error"] = 1
                            ret["message"] = "Type error!" 
                else:
                    ret["error"] = 1
                    ret["message"] = "Params error!" 
            else:
                ret["error"] = 1
                ret["message"] = "Check error!" 
        else:
            ret["error"] = 1
            ret["message"] = "Cannot Upload!" 
            
        info = json.dumps(ret) 
        self.write(info)

        pass

if __name__ == "__main__":
    print
    