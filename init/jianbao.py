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
        js_p = js_content.find_all('p')
        content = ''
        for cont in js_p:
            for st in cont.stripped_strings:
                content = content + st + '\n' 
        lines =content.replace(u'(公众号:第壹简报)', '').replace('\n\n','\n').split("\n")[0:14]
        out_content = ''
        for line in lines:
            if not out_content:
                out_content = out_content + line
            else:
                out_content = out_content + "\n" +  line
        return out_content   


if __name__ == '__main__':
    #jianbao_url = 'https://mp.weixin.qq.com/s/5E_SGRmaDA9O1nZgjGG0mw'
    #jianbao_url = 'http://mp.weixin.qq.com/s?__biz=MzA4NjU4ODY0Mg==&mid=2247485085&idx=1&sn=b58b653ff2c6d685f2964687d90a7b35&chksm=9fc72b10a8b0a206605854cefeaaa9f9568c996c4e2affdf01aa9c6ab261710488a14f0179f0&scene=0#rd'
    jianbao_url = 'http://mp.weixin.qq.com/s?__biz=MzA4NjU4ODY0Mg==&mid=2247485089&idx=1&sn=ab5db64bd61b90166b8f962c0eede624&chksm=9fc72b2ca8b0a23a94b14a6bc53a254a76c69b38aef469264bacb1f8109cfa82276e169a1fe6&scene=0#rd'
    jb = Get_Jianbao(jianbao_url)
    content = jb.out_jianbao()
    print content
