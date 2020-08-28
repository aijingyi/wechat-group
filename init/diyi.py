#coding:utf-8


import re
import urllib
from bs4 import BeautifulSoup
import datetime

class Get_Jianbao():
    def __init__(self,jianbao_url):
        self.jianbao_url = jianbao_url
        self.day = datetime.datetime.now().strftime("%d")
        #month = datetime.datetime.now().strftime("%m")
        #self.head_num = u"月%s日" % (day )
        #print self.head_num

    def get_html(self):
        response = urllib.request.urlopen(self.jianbao_url)
        html = response.read()
        #print html
        return html
    def out_jianbao(self):
        soup = BeautifulSoup(self.get_html(), "html.parser")
        js_content = soup.find(id='js_content')
        js_p = js_content.find_all('p')
        content = ''
        for cont in js_p:
            for st in cont.stripped_strings:
                content = content + st + '\n' 
        #print content
        lines =content.replace(u'公众号ID：dailynews001', '').replace('\n\n','\n')\
.replace('12\n','12').replace('2\n','2').replace('10\n','10')\
.replace('11\n', '11').replace('12\n', '12').split("\n")
        #print(len(lines))
        #for i in lines:
            #print(i)
        for num in range(0,75):
            if u"日第壹简报"  in lines[num]:
                ln1 = num
                break 
        for num in range(0,40):
            if u'【心语】' in lines[num]:
                ln2 = num
                break 
        lines = lines[ln1 :  ln1 + 20]
        #print lines
        out_content = ''
        for line in lines:
            if not out_content:
                out_content = out_content + line
            else:
                out_content = out_content + "\n" +  line
        return out_content   


if __name__ == '__main__':
    jianbao = []
    #jianbao.append('https://mp.weixin.qq.com/s/_YNcV5iT_PwBlz-I6D0Yxg')
    #jianbao.append('https://mp.weixin.qq.com/s/rXUUdM_wuERPpm2u65WzsA')
    #jianbao.append('https://mp.weixin.qq.com/s/fQ_oOcL4bscvz1ksGe5oSg')
    #jianbao.append('https://mp.weixin.qq.com/s/8kW_WETToHGcAOGZZKwFcg')
    jianbao.append('https://mp.weixin.qq.com/s/mewxjcZjmyhHblik3SQ7eA')
    for jianbao_url in jianbao:
        jb = Get_Jianbao(jianbao_url)
        content = jb.out_jianbao()
        print(content)
