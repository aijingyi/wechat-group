#/usr/bin/env python
#coding:utf-8
import logging,logging.handlers
import os

if not os.path.exists('log'):
    os.mkdir('log')
log_filename = "log/wechat.log"
log_level = logging.DEBUG
format = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)2d]-%(funcName)s %(levelname)s %(message)s')
handler = logging.handlers.RotatingFileHandler(log_filename, mode='a', maxBytes=10*1024*1024, backupCount=5)
handler.setFormatter(format)
logger = logging.getLogger('log')
logger.addHandler(handler)
logger.setLevel(log_level)

if __name__ == "__main__":
    WriteLog().info('123') #模块内部直接调用函数。等价下面两行,下面的方法不推荐
    # writelog = WriteLog('api')
    # writelog.info('123')
