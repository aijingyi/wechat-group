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
        lines =content.replace(u'（公众号：简报微刊）', '').replace('\n\n','\n')\
.replace('12\n','12').replace('2\n','2').split("\n")
        for num in range(0,40):
            if u'日简报微刊' in lines[num]:
                ln1 = num
                break 
        for num in range(0,40):
            if u'【微语】' in lines[num]:
                ln2 = num
                break 
        lines = lines[ln1 : ln2 + 1]
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
    #jianbao.append('https://mp.weixin.qq.com/s/QfRSelJSNkHa6la9rIphDA')
    #jianbao.append('https://mp.weixin.qq.com/s/1PhxnsY1i5nA0mEUbaab1Q')
    #jianbao.append('https://mp.weixin.qq.com/s/XfeZm1GL8I6gW405PAkmRQ')
    #jianbao.append('https://mp.weixin.qq.com/s/A_5hMZG2mzAn1HRnKOttrA')
    jianbao.append('https://mp.weixin.qq.com/s/m1-m9yK0_bvuleoDX6Am2Q')
    for jianbao_url in jianbao:
        jb = Get_Jianbao(jianbao_url)
        content = jb.out_jianbao()
        print content
