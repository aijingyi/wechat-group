#coding:utf-8

#analyze group log
import os
import time
import datetime
import sys

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
        self.logtxt =  str(self.day) + '.txt'
        self.talktxt = self.group_name + '_' + str(self.day) + '.txt'
        self.time_year = time.strftime("%Y-", time.localtime())

    #记录当天群成员名字        
    def log_members(self,members):
        member_log = self.group_name +'_' +  str(self.today) + '_member.txt'
        member_file = os.path.join(self.talk_path,member_log)
        with open(member_file,'w') as f:
            for i in members:
                f.write(i)
                f.write('\n')
    #输出昨天群成员名字
    def output_members(self):
        member_log = self.group_name + '_' +  str(self.day) + '_member.txt'
        member_file = os.path.join(self.talk_path,member_log)

        if not os.path.exists(member_file):
            return 0
        member_list = []
        with open(member_file,'r') as f:
            
            for i in f.readlines():
                member_list.append(i.strip('\n'))
            return member_list
       

    #聊天记录排行榜
    def log_context(self):
        file_path = os.path.join(self.path,self.group_name,self.logtxt) 
        #print file_path
        try:
            logfile = open(file_path,'r')
        except:
            return [0,0,'无聊天记录。']
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
        talks.writelines('昨天聊天排行榜TOP10（昵称   次数）\n\n')
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
        return peoples_nums,nums, top_contents
         







if __name__ == "__main__":
    grouplog = GroupLog('ce-shi-zhuan-yong-qun','log')
    nums = grouplog.log_context()
    #print nums
