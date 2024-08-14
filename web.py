# -*- coding: utf-8 -*-

import os, sys, signal
import logging
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado.options import define, options
from application import Application
import settings
import time

def check_command_line():
    
    if not options.port :
        raise ValueError, "The port is need!"
    
    if options.id < 0 :
        raise ValueError, "The shard id is need!"
    settings.SHARD_ID = options.id
    
    def check_path(type, path_list):
        if len(path_list) > 2 :
            raise ValueError, "Path list is error!"

        i = 0
        for x in path_list :
            if x and not os.path.exists(x.decode('utf-8').encode(sys.getfilesystemencoding())):
                raise ValueError, "The directory does not exist: " + x
            elif x :
                (settings.SHARD_CONFIG.get(type))[['path', 'bak_path'][i]] = x
                i += 1

    if options.p : check_path("p", options.p)
    if options.a : check_path("a", options.a)
    if options.v : check_path("v", options.v)
    if options.f : check_path("f", options.f)
    
    settings.ENV = options.env
    
    logging.warning("shard_id : " + str(settings.SHARD_ID))
    logging.warning("shard_config : " + str(settings.SHARD_CONFIG))
    logging.warning("runtime env : " + str(settings.ENV))


def config_log():
    # need the path of logs
    #if not os.path.exists(options.logPath.decode('utf-8').encode(sys.getfilesystemencoding())):
    #    raise ValueError, "The directory does not exist: " + options.logPath
    
    if not options.logPath:
        raise ValueError, "The directory does not exist: " + options.logPath
    
    if not os.path.exists(options.logPath.decode('utf-8').encode(sys.getfilesystemencoding())):
        os.makedirs(options.logPath.decode('utf-8').encode(sys.getfilesystemencoding()), mode=0777)
        os.chmod(options.logPath.decode('utf-8').encode(sys.getfilesystemencoding()), stat.S_IRWXU | stat.S_IRWXO | stat.S_IRWXG)

    log_fmt = tornado.log.LogFormatter(color=False,
        fmt=r'[%(asctime)s - %(name)s - %(process)s] [%(levelname)8s] [%(filename)s:%(lineno)s] - %(message)s',
        datefmt=r'%Y-%m-%d,%H:%M:%S')
    
    # access log
    channel = logging.handlers.TimedRotatingFileHandler(
        os.path.join(options.logPath, 'access.log'),
        'midnight',
        1, 0)
    channel.setFormatter(log_fmt)
    logging.getLogger("tornado.access").addHandler(channel)
    logging.getLogger("tornado.access").propagate = False
    
    # root (WARNING)
    logger = logging.getLogger()
    # default: WARNING
    channel = logging.handlers.TimedRotatingFileHandler(
        os.path.join(options.logPath, 'root.log'),
        'midnight',
        1, 0)
    channel.setFormatter(log_fmt)
    logger.addHandler(channel)
    
    # default (INFO)
    logger = logging.getLogger("DEFAULT")
    logger.setLevel(logging.INFO)
    channel = logging.handlers.TimedRotatingFileHandler(
        os.path.join(options.logPath, 'common_default.log'),
        'midnight',
        1, 0)
    channel.setFormatter(log_fmt)
    logger.addHandler(channel)
    
    # error (ERROR)
    logger = logging.getLogger("ERROR")
    logger.setLevel(logging.ERROR)
    channel = logging.handlers.TimedRotatingFileHandler(
        os.path.join(options.logPath, 'common_error.log'),
        'midnight',
        1, 0)
    channel.setFormatter(log_fmt)
    logger.addHandler(channel)

def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    logging.warning('Stopping http server')
    server.stop() # cannot accept http request
    logging.warning('Will shutdown in %s seconds ...', 5) #settings.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN
    io_loop = tornado.ioloop.IOLoop.instance()
    deadline = time.time() + 5

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop() # 处理完现有的 callback 和 timeout 后，可以跳出 io_loop.start() 里的循环
            logging.warning('Shutdown')
    
    stop_loop()
    logging.shutdown()

if __name__ == "__main__":

    #catch TERM and INT
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    
    # prepare configuration
    tornado.options.parse_command_line()
    config_log()
    check_command_line()

    application = Application()
    server = tornado.httpserver.HTTPServer(application)
    server.listen(options.port)
    logging.warning('Web starting: %s', options.port)
    tornado.ioloop.IOLoop.instance().start()

    logging.warning('Exit')
    logging.shutdown()
    
