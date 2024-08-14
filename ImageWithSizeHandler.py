# -*- coding: utf-8 -*-

import tornado.web
import os
import hashlib
import random
import json
import sys
import stat
import time
from pgmagick import Image
import settings
from AuthFilter import AuthFilter
from AbstractImageHandler import AbstractImageHandler

class ImageWithSizeHandler(AbstractImageHandler):

    def write_file(self, file_dir, group, first_d, second_d, third_d, content, name, end):
        new_d = os.path.join(file_dir, group, first_d, second_d, third_d)
        if not os.path.exists(new_d.decode('utf-8').encode(sys.getfilesystemencoding())):
            os.makedirs(new_d.decode('utf-8').encode(sys.getfilesystemencoding()), mode=0777)
            os.chmod(new_d.decode('utf-8').encode(sys.getfilesystemencoding()), stat.S_IRWXU | stat.S_IRWXO | stat.S_IRWXG)
                            
        dst = os.path.join(new_d, name + '.' + end)

        (lambda f, d: (f.write(d), f.close()))(open(dst.decode('utf-8').encode(sys.getfilesystemencoding()), 'wb+'), content)        
        
        im = Image(dst.decode('utf-8').encode(sys.getfilesystemencoding()))
        #str
        (xx, yy) = (str(im.columns()), str(im.rows()))
        #print xx, yy
        dst = os.path.join(new_d, name + '_' + xx + 'x' + yy +'.' + end)
        im.write(dst.decode('utf-8').encode(sys.getfilesystemencoding()))
        
        return [xx, yy]
        #return [None, None]

