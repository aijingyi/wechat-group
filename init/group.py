#!/usr/bin/env python
#coding: utf-8

#from __future__ import division
import os
import time
import datetime
import threading
import schedule
import ConfigParser
import re
import sys
import hashlib
import random
from wxpy import *
#from xpinyin import Pinyin


from init import analyze
#from init import express
from init.logger import logger
from init import xiaoyu
from init import xiaodou
from init import jianbao

reload(sys)
sys.setdefaultencoding('utf8')



class GroupMessage():
    #从配置文件获取参数，初始化变量
    def __init__(self):
        self.log_flag = 0
        cf = ConfigParser.ConfigParser()
        if os.path.exists('config/my.conf'):
            cf.read('config/my.conf')
        else:
            cf.read('config/wechat.conf')
        self.path = cf.get('wechat', 'path')
        group_names = cf.get('wechat', 'group_name').decode('utf-8')
        self.group_list=group_names.strip(',').split(',')
        self.friend_name = cf.get('wechat','friends').decode('utf-8')
        self.newcomer = cf.get('wechat','newcomer')
        self.recev_mps = int(cf.get('wechat','recev_mps'))
        self.use_xiaoi = int(cf.get('wechat','xiaoi'))
        self.key = cf.get('wechat','key')
        self.secret = cf.get('wechat','secret')
        self.xiaodou_key = cf.get('wechat','xiaodou_key')
    
        self.send_msg = u'早上好'
        self.send_night = u'晚安哦'
        group_note = cf.get('wechat', 'group_note').decode('utf-8')
        self.group_note_list=group_note.strip(',').split(',')
        group_jianbao = cf.get('wechat', 'group_jianbao').decode('utf-8')
        self.group_jianbao_list=group_jianbao.strip(',').split(',')
        group_newcomer = cf.get('wechat', 'group_newcomer').decode('utf-8')
        group_newcomer1 = cf.get('wechat', 'group_newcomer1').decode('utf-8')
        self.group_newcomer_list=group_newcomer.strip(',').split(',')
        self.group_newcomer_list1=group_newcomer1.strip(',').split(',')
        self.send_time = cf.get('wechat', 'send_time').decode('utf-8')
        self.send_talks = cf.get('wechat', 'send_talks').decode('utf-8')
     
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.talk_path = os.path.join(self.path, 'talks')
        if not os.path.exists(self.talk_path):
            os.mkdir(self.talk_path)
        self.members_path = os.path.join(self.path, 'members')
        if not os.path.exists(self.members_path):
            os.mkdir(self.members_path)


        self.xiaoi = XiaoI(self.key, self.secret)
        self.xiaoyuer = xiaoyu.XiaoY()
        self.xiaodou = xiaodou.Xiaodou(self.xiaodou_key)

        self.send_me = 1

    def init_group_name(self):
        self.group__newcomer = []


    def login(self):
        self.bot = Bot(cache_path=True, console_qr=True)
        #self.bot.enable_puid()
        self.myself = self.bot.self
        try:
            self.friend = self.bot.friends().search(self.friend_name)[0]
        except:
            self.friend = self.bot.self
     
        #print self.bot.friends()
        #logger.info(self.bot.groups())
        #print self.bot.mps()

    def create_group_logfile(self):
        group = self.bot.groups(update=True)
        logger.info(group)
        for gs in group:
            group_name = hashlib.md5(gs.name.encode('utf-8')).hexdigest()[-8:]
            logger.info(gs)
            logger.info(group_name)
            log_file = os.path.join(self.path,group_name)
            if not os.path.exists(log_file):
                os.mkdir(log_file)
        

    def send_friend_msg(self,send_friend,send_msg):
        logger.info(send_friend)
        self.friend_chuxin = self.bot.friends().search(send_friend)[0]
        self.friend_chuxin.send(send_msg)
    def send_kevin_msg(self):
        now_time = time.asctime( time.localtime(time.time()) )
        self.kevin_m = self.bot.friends().search('Kevin')[0]
        self.kevin_m.send(now_time)

    def send_group_msg(self,send_msg):
        self.group_jiaoyou = self.bot.groups().search(u'北京交友群')[0]
        #self.group_jiaoyou = self.bot.groups().search(u'测试专用群')[0]
        self.group_jiaoyou.send(send_msg)

    def read_topic(self):
        topic_f = open("material/topic.txt","r")
        comment = topic_f.readlines()
        comment_filter = []
        for co in comment:
            if not co.startswith('#'):
                comment_filter.append(co)
        #print len(comment_filter)
        #one_topic = comment_filter[random.randint(0,len(comment)-1)]
        return comment_filter

    def msg_from_friends(self):
        @self.bot.register(Friend)
        def msg_yy(msg):
            """
            微信web版无法邀请好友入群
            if msg.text == u'北京':
                msg.reply('北京交流群')    
                new_friend = self.bot.friends().search(msg.sender.name)[0]
                group_beijing = self.bot.groups().search(u'北京交流群')[0]
                group_beijing.add_members(new_friend, use_invitation=True)
            elif msg.text == u'小群':
                msg.reply('北京小群')    
                group_tianjin = self.bot.groups().search(u'人工智能体验群')[0]
                new_friend = self.bot.friends().search(msg.sender.name)[0]
                self.friend.send(new_friend)
                group_tianjin.add_members(new_friend, use_invitation=True)
            """
            if msg.sender.name == 'Kevin':
                try:
                    send_kevin =12
                    if send_kevin == 1:
                        msg.reply('Hello')
                except Exception as e:
                    logger.error(e)
            else:
                if msg.text == u'你好':
                    try:
                        msg.reply(u'你好')
                    except Exception as e:
                        logger.error(e)

    #处理公共号消息
    def my_mps(self):
        @self.bot.register(MP)
        def print_mp_msg(msg):
            #self.friend.send(msg)
            #self.friend.send_raw_msg( raw_content=msg.raw)
            #msg.forward(self.friend)
            """
            if msg.type == SHARING and msg.sender.name == '爱净意':
                for article in msg.articles:
                    if '第壹简报' in article.title:
                        self.friend.send(article.title)
                        self.friend.send(article.url)
                        #article_url = 'https://mp.weixin.qq.com/s/5E_SGRmaDA9O1nZgjGG0mw'
                        jb = jianbao.Get_Jianbao(article.url)
                        jb_content = jb.out_jianbao()
                        logger.info(jb_content)
                        self.friend.send(jb_content)
            if msg.type == SHARING and msg.sender.name == '硕士博士俱乐部':
                for article in msg.articles:
                    if '妹子篇' in article.title:
                        self.friend.send(article.title)
                        self.friend.send(article.url)
            if msg.type == SHARING and msg.sender.name == '硕博联谊':
                for article in msg.articles:
                    if  '妹子' in article.title and '现居北京' in article.title:
                        self.friend.send(article.title)
                        self.friend.send(article.url)
            """
            if msg.type == SHARING and msg.sender.name == '零点简报':
                for article in msg.articles:
                    if '简报微刊' in article.title:
                        #self.friend.send(article.title)
                        #self.friend.send(article.url)
                        jb = jianbao.Get_Jianbao(article.url)
                        jb_content = jb.out_jianbao()
                        self.jb_content = jb_content
                        #self.friend.send(jb_content)

                        for group_n in self.group_jianbao_list:
                            try:
                                my_group = self.bot.groups().search(group_n)[0]
                                my_group.send(jb_content)
                            except IndexError,e:
                                logger.error('%s not exists, please check it!' %val)


    
    def msg_from_friends_accept(self):
        @self.bot.register(msg_types=FRIENDS)
        def auto_accept_friends(msg):
            logger.info("enter accept")
            #new_friend = self.bot.accept_friend(msg.card)
            new_friend = msg.card.accept()
            new_friend.send('你好，欢迎加入北京交友群，此群用于聊天交友，不要发布支付宝红包、广告、砍价等信息哦。同意进群请回复"是"')
            logger.info("after accept")
            
            
    #处理群消息
    def group_msg(self):
        #注册消息
        @self.bot.register(Group)
        def print_msg(msg):
            #日志文件创建
            group_name = hashlib.md5(msg.sender.name.encode('utf-8')).hexdigest()[-8:]
            log_file = os.path.join(self.path,group_name)
            #print group_name
            day = time.strftime("%Y-%m-%d")
            file_name = '%s.txt' % ( day)
            file_ab_path = os.path.join(log_file, file_name)
            #pic_file = 'log/%s-%s' % (group_zh_name,day)
            pic_file = os.path.join(self.path,group_name,day)
            if not os.path.exists(pic_file):
                os.mkdir(pic_file)
    
            create_time = msg.create_time.strftime('%Y-%m-%d %H:%M:%S')
            #name = msg.member.name
            name = msg.member.nick_name
            #群内有被at的消息就会智能回复，支持图灵和小i机器人，默认小i
            #print msg.is_at
            #print self.use_xiaoi
            #if msg.is_at and self.use_xiaoi == 1:
            myword = ''
            #消息处理，TEXT文本，SHARING链接，PICTURE图片，RECORDING语音，
            #ATTACHMENT附件，NOTE红包提示，新人入群提示，MAP地图
            #print PICTURE, VIDEO,RECORDING,ATTACHMENT
            if msg.type == TEXT:
                word = "%s %s:%s\n" % (create_time, name, msg.text)
                if msg.is_at or msg.text.startswith(u'小鱼儿'):
                    #tuling = Tuling(api_key=self.key)
                    ret_text, self.use_xiaoi = self.xiaoyuer.do_reply(msg,self.use_xiaoi)
              
                    #小豆机器人
                    if ret_text == '1' and self.use_xiaoi == 1:
                        ret_text = self.xiaodou.do_reply(msg)
                    if ret_text == '2' and self.use_xiaoi == 1:
                        ret_text = self.xiaoi.do_reply(msg)
                        #ret_text = tuling.do_reply(msg)
                    myword = "%s %s:%s\n" % (create_time, self.myself.name, ret_text)
                
            elif msg.type == SHARING:
                #print  msg
                word = "%s %s:SHARING:%s\n" % (create_time, name, msg.text)
                
            elif msg.type in [PICTURE, VIDEO,RECORDING,ATTACHMENT]:
                ct = msg.create_time.strftime('%Y-%m-%d-%H-%M-%S')
                if msg.type == PICTURE:
                    msg.get_file('%s/%s-%s-%s' % (pic_file,ct,random.randint(1,10),msg.file_name))
                    word = "%s %s:PICTURE:%s\n" % (create_time, name, msg.file_name)
                #elif msg.type == VIDEO:
                 #  msg.get_file('%s/%s-%s-%s' % (file_name,ct,name,msg.file_name))
                elif msg.type == RECORDING:
                    #print name
                    msg.get_file('%s/%s-%s-%s' % (pic_file,ct,name,msg.file_name))
                    word = "%s %s:RECORDING:%s\n" % (create_time, name, msg.file_name)
                elif msg.type == ATTACHMENT:
                    #print msg.file_name
                    msg.get_file('%s/%s-%s-%s' % (pic_file,ct,name,msg.file_name))
                    word = "%s %s:ATTACHMENT:%s\n" % (create_time, name, msg.file_name)
            elif msg.type == NOTE:
                #self.friend.send(word)
                if u'\u6536\u5230' in msg.text:
                    #print 'red packages!!!!!!!!!!!!!!!!!!!!!!'
                    self.friend.send('Red Package:%s' %(msg.sender.name))
                elif u'\u9080\u8bf7' in msg.text and self.newcomer == '1':
                    if group_name in self.group_newcomer_list: 
                        new_name = msg.text.split('"')[-2]
                        new_name_1 = None
                    elif group_name in self.group_newcomer_list1: 
                        #self.friend.send(self.group_newcomer_list1)
                        new_name_1 = msg.text.split('"')[-2]
                        new_name = None
                elif u'\u626b\u63cf' in msg.text and self.newcomer == '1':
                    if group_name in self.group_newcomer_list: 
                        new_name = msg.text.split('"')[1]
                        new_name_1 = None
                    elif group_name in self.group_newcomer_list1: 
                        new_name = None
                        new_name_1 = msg.text.split('"')[1]
                else:
                    new_name = new_name_1 = None
                
                if new_name:
                    newcomer_msg = """@%s 欢迎新人进群交友聊天，请详细阅读群公告。\n进群请修改备注：昵称-出生年-性别-职业（学生）-学历，如：\n%s-90-男-IT-硕士"""% (new_name, new_name)
                    msg.reply(newcomer_msg)
                elif new_name_1:
                    newcomer_msg_1 = """@%s 欢迎新人进群交友聊天，本群是跳转群，请加我好友拉你进大群。"""% (new_name_1)
                    msg.reply(newcomer_msg_1)
                word = "%s %s:NOTE:%s\n" % (create_time, name, msg.text)
            elif msg.type == CARD:
                word = "%s %s:CARD:%s\n" % (create_time, name, msg.text)
            elif msg.type == MAP:
                word = "%s %s:MAP:%s\n" % (create_time, name, msg.text)
            elif msg.type == SYSTEM:
                word = "%s %s:SYSTEM:%s\n" % (create_time, name, msg.text)
    
            if word:
                with open(file_ab_path, "a+") as f:
                    f.write(word.encode('utf-8'))
                    if myword:
                        f.write(myword.encode('utf-8'))
                    word = None
            #msg.forward(self.friend)
    #记录日志
    def log_message(self,group_name, word):
        log_file = os.path.join(self.path,group_name)
        if not os.path.exists(log_file):
            os.mkdir(log_file)
        

        #日志文件创建
        day = time.strftime("%Y-%m-%d")
        file_name = '%s.txt' % ( day)
        file_ab_path = os.path.join(log_file, file_name)
        pic_file = os.path.join(self.path,group_name,day)
        if not os.path.exists(pic_file):
            os.mkdir(pic_file)
    
        with open(file_ab_path, "a+") as f:
            f.write(word.encode('utf-8'))
            word = None


    #发送定时任务
    def send_message(self):
        #self.group_note_list  = [u'测试专用群']
        #print self.group_note_list
        for group_n in self.group_note_list:
            try:
                my_group = self.bot.groups().search(group_n)[0]
            except IndexError,e:
                logger.error('%s not exists, please check it!' %group_n)
                continue

            #group_name = hashlib.md5(my_group.name.encode('utf-8')).hexdigest()[-8:]
            group_members = analyze.GroupMembers(self.path, my_group) 
            group_members.analyze_mem()

            '''  
            elif self.send_me ==11:
                #my_group.send(group_mem_stats)
                create_time = time.strftime('%Y-%m-%d %H:%M:%S')
                #my_group.send_image('material/zaoan.png')
                #my_group.send('早上好！')
                word = "%s %s:Good Morning!\n" % (create_time, self.myself.name)
                self.log_message(group_name, word)
                if self.send_talks == "1":
                    for group_num in [member_word, talks_total]:
                        time.sleep(2)
                        my_group.send(group_num)
                    word = "%s %s:%s\n" % (create_time, self.myself.name, member_word)
                    self.log_message(group_name, word)
                    #word = "%s %s:%s\n" % (create_time, self.myself.name, print_nums)
                    #self.log_message(group_zh_name, word)
                    word = "%s %s:%s\n" % (create_time, self.myself.name, talks_total)
                    self.log_message(group_name, word)
            ''' 
    #使用schedule模块执行定时任务
    def use_sche(self):
        #if self.send_me == 1:
        #self.send_message()
        #schedule.every().day.at("17:17").do(self.send_message)
        schedule.every(10).minutes.do(self.send_message)
        schedule.every().day.at("7:30").do(self.send_group_msg,u'早上好')
        #schedule.every().day.at("9:30").do(self.send_group_msg,self.read_topic())
        #schedule.every().day.at("13:30").do(self.send_group_msg,self.read_topic())
        #schedule.every().day.at("17:30").do(self.send_group_msg,self.read_topic())
        #schedule.every(1).minutes.do(self.send_group_msg,self.read_topic()[random.randint(0,len(self.read_topic())-1)])
        
        while True:
            #self.myself.send('log out')
            if not self.bot.alive:
                logger.error('not login')
                self.main()
                break
            schedule.run_pending()
            time.sleep(10)
        

    #进入群聊接受消息 
    def run_task(self):            
        #self.msg_from_friends_accept()
        self.msg_from_friends()
        self.create_group_logfile()
        #my_groups = []
        self.group_msg()

        while True:
            if not self.bot.alive:
                logger.info('not login')
                self.main()
                break
            time.sleep(10)
        
        #embed()
        #self.bot.join()
            
    def main(self):
        self.login()
        #threads = []
        if self.recev_mps == 1:
            t1 = threading.Thread(target=self.my_mps,args=())
            t1.setDaemon(True)
            t1.start()

        t2 = threading.Thread(target=self.use_sche,args=())
        #t2.setDaemon(True)
        t2.start()
        t3 = threading.Thread(target=self.run_task,args=())
        #t3.setDaemon(True)
        t3.start()

if __name__ == "__main__":
    group_m = GroupMessage()
    group_m.main()   

