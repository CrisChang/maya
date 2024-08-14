# -*- coding: utf-8 -*-

import tornado.web
import os
import hashlib
import random
import json
import sys
import stat
import time
import settings
from AuthFilter import AuthFilter

class AudioHandler(tornado.web.RequestHandler):
    def initialize(self, bak_path = None, path = None, auth = None):
        if not path :
            self.open_flag = False
            self.file_dir = None
        else :
            self.open_flag = True
            self.file_dir = os.path.join(path, "audio")
            
        if bak_path:
            self.bak_path = os.path.join(bak_path, "audio")
        else:
            self.bak_path = None
            
        if auth:
            self.auth_filter = auth
        else :
            self.auth_filter = None

        self.return_url_prefix = "http://a" + str(settings.SHARD_ID)
        pass
    
    def get(self, group='common'):
        self.write("upload_audio: " + group)
        pass
        
    def write_file(self, file_dir, group, first_d, second_d, third_d, content, rename):
        new_d = os.path.join(file_dir, group, first_d, second_d, third_d)
        if not os.path.exists(new_d.decode('utf-8').encode(sys.getfilesystemencoding())):
            os.makedirs(new_d.decode('utf-8').encode(sys.getfilesystemencoding()), mode=0777)
            os.chmod(new_d.decode('utf-8').encode(sys.getfilesystemencoding()), stat.S_IRWXU | stat.S_IRWXO | stat.S_IRWXG)
                            
        dst = os.path.join(new_d, rename)

        (lambda f, d: (f.write(d), f.close()))(open(dst.decode('utf-8').encode(sys.getfilesystemencoding()), 'wb+'), content)        
        pass

    def post(self, group='common'):
        ret = {
            "error" : 0, 
            "message" : [] 
        }

        if self.open_flag:
            if self.auth_filter and self.auth_filter.doFilter(self):
                
                if self.request.files:
                    for f in self.request.files["files"]:
                        try: 
                            rawname = f['filename'].encode('UTF-8')
                            [front, end] = rawname.rsplit('.', 1)
                            
                            if True or end in [] :
                                m = hashlib.md5()
                                m.update(front + str(int(time.time())) + str(random.random()))
                                m.digest()
                                m = m.hexdigest()
                                [first_d, second_d, third_d, name] = [m[0:2], m[2:4], m[4:6], m]
            
                                rename =  name + '.' + end
                                
                                self.write_file(self.file_dir, group, first_d, second_d, third_d, f['body'], rename)
                                
                                if self.bak_path:
                                    self.write_file(self.bak_path, group, first_d, second_d, third_d, f['body'], rename)
                                
                                if settings.ENV == 'product':
                                    ret["message"].append(self.return_url_prefix  + settings.DOMAIN  + "/audio/" + group + "/" + rename)
                                elif settings.ENV == 'idc_test':
                                    ret["message"].append('http://' + settings.IDC_TEST_IP + "/audio/" + group + "/" + rename)
                                elif settings.ENV == 'test':
                                    ret["message"].append('http://' + settings.TEST_IP + "/audio/" + group + "/" + rename)
                                else:
                                    ret["message"].append('The env is error!')
                            else:
                                ret["error"] = 1
                                ret["message"] = "Type error!" 
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

