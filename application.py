# -*- coding: utf-8 -*-

import os, sys, signal
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
import settings
from tornado.options import define, options
from ImageHandler import ImageHandler
from AudioHandler import AudioHandler
from VideoHandler import VideoHandler
from FileHandler import FileHandler
from AuthFilter import AuthFilter
from ImageWithSizeHandler import ImageWithSizeHandler
from FastImageHandler import FastImageHandler
from ImageFixUrlHandler import ImageFixUrlHandler

define("id", default=None, help="Config of shard id.", type=int)
define("port", default=None, help="Run server on a specific port.", type=int)
define("logPath", default=None, help="Config of the paht of logs.", type=str)
define("env", default="product", help="Config of runtime env.", type=str, metavar="test|idc_test|product")
define("p", default=None, help="Config of picture.", type=str, multiple=True)
define("a", default=None, help="Config of audio.", type=str, multiple=True)
define("v", default=None, help="Config of vedio.", type=str, multiple=True)
define("f", default=None, help="Config of file.", type=str, multiple=True)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello world!")
        
authFilter = AuthFilter()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
        (r"/", MainHandler),
        (r"/upload_image.do", ImageHandler, dict(settings.SHARD_CONFIG.get('p'), **{'auth':authFilter})),
        (r"/(\w+)/upload_image.do", ImageHandler, dict(settings.SHARD_CONFIG.get('p'), **{'auth':authFilter})),
        #(r"/fast_image.do", FastImageHandler, dict(settings.SHARD_CONFIG.get('p'), **{'auth':authFilter})),
        #(r"/(\w+)/fast_image.do", FastImageHandler, dict(settings.SHARD_CONFIG.get('p'), **{'auth':authFilter})),
        #(r"/upload_image_fixurl.do", ImageFixUrlHandler, dict(settings.SHARD_CONFIG.get('p'), **{'auth':authFilter})),
        (r"/upload_image_s.do", ImageWithSizeHandler, dict(settings.SHARD_CONFIG.get('p'), **{'auth':authFilter})),
        (r"/(\w+)/upload_image_s.do", ImageWithSizeHandler, dict(settings.SHARD_CONFIG.get('p'), **{'auth':authFilter})),
        (r"/upload_audio.do", AudioHandler, dict(settings.SHARD_CONFIG.get('a'), **{'auth':authFilter})),
        (r"/(\w+)/upload_audio.do", AudioHandler, dict(settings.SHARD_CONFIG.get('a'), **{'auth':authFilter})),
        (r"/upload_video.do", VideoHandler, dict(settings.SHARD_CONFIG.get('v'), **{'auth':authFilter})),
        (r"/(\w+)/upload_video.do", VideoHandler, dict(settings.SHARD_CONFIG.get('v'), **{'auth':authFilter})),
        (r"/upload_file.do", FileHandler, dict(settings.SHARD_CONFIG.get('f'), **{'auth':authFilter})),
        (r"/(\w+)/upload_file.do", FileHandler, dict(settings.SHARD_CONFIG.get('f'), **{'auth':authFilter})),
        ]
        
        #ui_modules = {
        #    'one': one,
        #    'two': two,
        #}
        
        tornado_settings = {
            #"static_path": os.path.join("/data", "static"),
        }
        
        tornado.web.Application.__init__(self, handlers, **tornado_settings)

# Notice: We need config arguments, so this line is to write in web.py
# application = Application()