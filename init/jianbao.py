#coding:utf-8


import re
import urllib2
from bs4 import BeautifulSoup

class Get_Jianbao():
    def __init__(self,jianbao_url):
        self.jianbao_url = jianbao_url

    def get_html(self):
        response = urllib2.urlopen(self.jianbao_url)
        html = response.read()
        return html
    def out_jianbao(self):
        soup = BeautifulSoup(self.get_html(), "html.parser")
        #print soup.prettify()
        #js_head = soup.find(id='activity-name')
        #for string in js_head.stripped_strings:
         #   head = string
        #print js_content.string 
        js_content = soup.find(id='js_content')
        #print js_content
        js_p = js_content.find_all('p')
        #print js_p
        content = ''
        for cont in js_p:
            for st in cont.stripped_strings:
                #print st
                content = content + st + '\n' 
        #lines =content.replace(u'(公众号:第壹简报)', '').replace('\n\n','\n').split("\n")[0:14]
        #print content
        lines =content.replace(u'(公众号:第壹简报)', '').replace('\n\n','\n').split("\n")
        for num in range(0,35):
            if u'来源: 澎湃新闻' in lines[num]:
                l_n = num
                break
        #print l_n
        l_n= l_n + 1
        lines = lines[l_n:l_n+17]
        #for i in lines:
         #   print i
        out_content = ''
        for line in lines:
            if not out_content:
                out_content = out_content + line
            else:
                out_content = out_content + "\n" +  line
        return out_content   


if __name__ == '__main__':
    jianbao = []
    #jianbao.append('https://mp.weixin.qq.com/s/5E_SGRmaDA9O1nZgjGG0mw')
    #jianbao.append('https://mp.weixin.qq.com/s/XiKzJWrid8bcA_hDO7ZIjA')
    #jianbao.append('https://mp.weixin.qq.com/s/UMKZjo2t6GRe--YJjxowug')
    #jianbao.append('https://mp.weixin.qq.com/s/boQCZsy7XRuiqZhhoM9nOA')
    #jianbao.append('https://mp.weixin.qq.com/s/sge8zhlL71yeBr0JZNI21A')
    #jianbao.append('https://mp.weixin.qq.com/s/e5nijc_xRvv4niufqnx5mA')
    jianbao.append('https://mp.weixin.qq.com/s/7yUF15misy-qwrY0TpdjFQ')

    for jianbao_url in jianbao:
        jb = Get_Jianbao(jianbao_url)
        content = jb.out_jianbao()
        print content
