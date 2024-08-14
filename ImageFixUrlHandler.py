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
import re
#from pgmagick import Image
import settings
from AuthFilter import AuthFilter

class ImageFixUrlHandler(tornado.web.RequestHandler):
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
    
    def get(self):
        self.write("upload_fixurl_image: ")
        pass

    def write_file(self, file_dir, group, first_d, second_d, third_d, content, name, end):
        new_d = os.path.join(file_dir, group, first_d, second_d, third_d)
        if not os.path.exists(new_d.decode('utf-8').encode(sys.getfilesystemencoding())):
            os.makedirs(new_d.decode('utf-8').encode(sys.getfilesystemencoding()), mode=0777)
            os.chmod(new_d.decode('utf-8').encode(sys.getfilesystemencoding()), stat.S_IRWXU | stat.S_IRWXO | stat.S_IRWXG)
                            
        dst = os.path.join(new_d, name + '.' + end)

        (lambda f, d: (f.write(d), f.close()))(open(dst.decode('utf-8').encode(sys.getfilesystemencoding()), 'wb+'), content)        

    def post(self):
        ret = {
            "error" : 0, 
            "message" : [] 
        }
        if self.open_flag:
            if self.auth_filter and self.auth_filter.doFilter(self):
                
                if self.request.files:
                    for f in self.request.files["files"]:
                        try: 
                            url = f['filename'].encode('UTF-8')
                            pattern = re.compile(r'image[/#](.+)[/#]([0-9a-f]{32})_(.+)\.(.+)')
                            rawname = pattern.findall(url)
                            if len(rawname) > 0:
                                group = rawname[0][0]
                                name = rawname[0][1]
                                size = rawname[0][2]
                                end = rawname[0][3]
                                first_d, second_d, third_d = name[0:2], name[2:4], name[4:6]
    
                                if True or end in [] :
                                    
                                    #file_url = os.path.join(self.file_dir, group, first_d, second_d, third_d, name + '.' + end)
                                    #if not os.path.exists(file_url.decode('utf-8').encode(sys.getfilesystemencoding())):
                                    self.write_file(self.file_dir, group, first_d, second_d, third_d, f['body'], name, end)
                                    self.write_file(self.file_dir, group, first_d, second_d, third_d, f['body'], name + '_' + size, end)
                                    
                                    if self.bak_path:
                                        self.write_file(self.bak_path, group, first_d, second_d, third_d, f['body'], name, end)
    
                                    rename = name + '_' + size +'.' + end
                                    
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
                                ret["message"] = "params error!"
                        except Exception,ex:
                            ret["error"] = 1
                            ret["message"] = str(ex)
                else:
                    ret["error"] = 1
                    ret["message"] = "No file error!" 
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
    url = 'http://112.126.68.72/image/common/22e56279a10ca7cc1fe19758e13e74d0_111x222.jpg'
    pattern = re.compile(r'image/(.+)/(.+)_(.+)\.(.+)')
    rawname = pattern.findall(url)[0]
    group = rawname[0]
    name = rawname[1]
    size = rawname[2]
    end = rawname[3]
    first_d, second_d, third_d = name[0:2], name[2:4], name[4:6]
    print group, first_d, second_d, third_d, name, size, end