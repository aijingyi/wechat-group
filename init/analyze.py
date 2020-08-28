#coding:utf-8

from wxpy import *

#analyze group log
import os
import time
import datetime
import sys
import hashlib
import json

#print sys.getdefaultencoding() 

class GroupLog():
    def __init__(self,group_name,path):
        self.path = path
        self.talk_path = os.path.join(self.path,'talks/')
        self.group_name = group_name
        #self.day = day = time.strftime("%Y-%m-%d")
        self.today=datetime.date.today() 
        self.oneday=datetime.timedelta(days=1) 
        self.day = self.today-self.oneday 
        self.logtxt =  str(self.today) + '.txt'
        self.talktxt = self.group_name + '_' + str(self.today) + '.txt'
        self.time_year = time.strftime("%Y-", time.localtime())


    #聊天记录排行榜
    def log_context(self):
        file_path = os.path.join(self.path,self.group_name,self.logtxt) 
        #print file_path
        try:
            logfile = open(file_path,'r')
        except:
            return u'今日无人发言。'
        context = logfile.readlines()
        logfile.close()
        #log_lines = len(context)
        nums = 0
        peoples = []
        for i in context:
            if i.startswith(self.time_year):
                #if 'PICTURE' in i or 'SHARING' in i:
                 #   peoples.append(i.split(':')[2][3:])
                  #  nums = nums +1
                if 'NOTE' not in i:
                    peoples.append(i.split(':')[2][3:])
                    nums = nums +1
        peoples_set = set(peoples)
        peoples_nums = len(peoples_set)
        peoples_dic = {}
        for i in peoples_set:
            peoples_dic[i] = peoples.count(i)
            #print("%s %d" %(i,peoples.count(i)))
        #print peoples_dic
        talks_file = self.talk_path + self.talktxt
        if os.path.exists(talks_file):
            os.remove(talks_file)
        talks = open(talks_file,'a')
        talks.writelines('今日聊天排行榜TOP10（昵称   次数）\n\n')
        i = 0
        for key,value  in sorted(peoples_dic.items(),key = lambda x:x[1],reverse = True):
            talks_txt = key + '    ' + str(value) + '\n'
            talks.writelines(talks_txt)
            if i >= 9:
                break
            i = i +1 
        talks.close()

        with open(talks_file,'r') as f:
            top_contents = f.read()
        #print top_contents
        if peoples_nums == 0:
            talks_total = '今日没有人发言。'
        else:
            print_nums = '今日有%s人在群内侃侃而谈%s句。' %(peoples_nums,nums)
            talks_total = print_nums + '\n\n' + top_contents
        return talks_total
         
class GroupMembers():
    def __init__(self,path,group, send_to_me):
        self.path = path
        self.talk_path = os.path.join(self.path,'members')
        self.group = group
        self.send_to_me = send_to_me
        self.members = group.members
        self.group_name = hashlib.md5(group.name.encode('utf-8')).hexdigest()[-8:]

    #记录当天群成员名字        
    def log_members(self):
        member_log = self.group_name  + '_member.json'
        member_file = os.path.join(self.talk_path,member_log)
        results = []
        num = 1
        for mem in self.members:
            temp = {}
            temp['id'] = num
            temp['name'] = mem.name
            temp['nick_name'] = mem.nick_name
            temp['user_name'] = mem.user_name
            num = num + 1
            results.append(temp)
    
        with open(member_file, "w") as f:
            # indent 超级好用，格式化保存字典，默认为None，小于0为零个空格
            f.write(json.dumps(results, indent=4))
            # json.dump(a,f,indent=4)   # 和上面的效果一样
        return results

    #输出昨天群成员名字
    def output_members(self):
        member_log = self.group_name  + '_member.json'
        member_file = os.path.join(self.talk_path,member_log)

        if not os.path.exists(member_file):
            self.log_members()
            return 0
        member_list = []
        with open(member_file, "r") as f:
            results = json.loads(f.read())
        #f.seek(0)
        #bb = json.load(f)    # 与 json.loads(f.read())
        return results
       
    def analyze_mem(self):
        results_old = self.output_members()
        results_new = self.log_members()
      
        if results_old == 0 or results_old == results_new:
            return False
        else:
            result_old_list = []
            result_new_list = []
            for old_re in results_old:
                #print old_re
                result_old_list.append(old_re['nick_name'])
            for new_re in results_new:
                result_new_list.append(new_re['nick_name'])
            #print result_old_list
            #print result_new_list
     
            out_mem = ''
            for i in result_old_list:
                if i not in result_new_list:
                    out_mem = out_mem + i + '，'
            if out_mem == '':
                return False
            print_out = u"%s 悄悄的离开了本群。" %(out_mem[:-1])
            self.send_to_me.send(print_out)
            #self.group.send(print_out)
            return print_out
                    



if __name__ == "__main__":
    #grouplog = GroupLog('c5fe69fa','log')
    #grouplog = GroupLog('9e3a6e4a','log')
    #nums = grouplog.log_context()
    #print nums
    bot = Bot(cache_path = False, console_qr = True)
    group = bot.groups().search(u'户外交友群')[0]
    group_mem = GroupMembers('log',group)
    print_out = group_mem.analyze_mem()
    if print_out:
        print(print_out)
