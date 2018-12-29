#coding:utf-8

import requests
from wxpy.api.messages import Message
from wxpy.ext.talk_bot_utils import get_context_user_id, next_topic
from wxpy.utils.misc import get_text_without_at_bot


class Xiaodou(object):
    """ xiaodou robot handler
    Referer: http://xiao.douqq.com
    """

    #HANDLE_MSGS = (TEXT, )
    DEFAULT_MSG = '2'

    KEY = 'http://api.douqq.com/?key=&msg=??'

    def __init__(self, key):
        self.key = key

    def match(self, msg):
        return True

    def do_reply(self, msg):
        que = [u'报时',u'每日一句',u'猜谜',u'糗事',u'空气质量',u'藏头诗',u'梦见',u'一言',u'什么是',u'脑筋急转弯']
        if isinstance(msg, Message):
            user_id = get_context_user_id(msg)
            if msg.text.startswith(u'小鱼儿'):
                question = msg.text.replace(u'小鱼儿','').strip()
            else:
                question = get_text_without_at_bot(msg)
        else:
            user_id = "abc"
            question = msg or ""
        url = 'http://api.douqq.com'
        params = {'key': self.key, 'msg': question}
        #params = {'key': self.key, 'msg': msg}
        #print question
        if question in que or u'求答案' in question or u'谜底' in question:
            try:
                resp = requests.get(url, params=params)
                ret = '@' + msg.member.name + ' ' + resp.text
                msg.reply(ret)
        #except requests.exceptions.RequestException:
            except:
                return self.DEFAULT_MSG
            return resp.text
        else:
            return self.DEFAULT_MSG

if __name__ == "__main__":
    key = 'dm9jcG09VW5JPWFOZ2g5SjdjUXZRbDRNbGhnQUFBPT0'
    xiaodou = Xiaodou(key)
    print xiaodou.handle('你好')
