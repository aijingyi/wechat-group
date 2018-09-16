#-*- coding:utf-8 -*-
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Make_express():
    def __init__(self):
        #设置所使用的字体
       self.a = 123 

    def set_font(self,num):
        return ImageFont.truetype("material/hanyi.ttf", num)

    def make_pic(self,words,pic_num):

        #打开图片
        if pic_num == '1':
            imageFile = "material/lsobel.jpg"
        else:
            imageFile = "material/background.jpg"
        im1 = Image.open(imageFile)

        #画图
        draw = ImageDraw.Draw(im1)
        if len(words) <= 3:
            draw.text((290, 600), words, (0, 0, 0), font=self.set_font(50))    #设置文字位置/内容/颜色/字体
        elif len(words) <= 5:
            draw.text((200, 600), words, (0, 0, 0), font=self.set_font(50))    #设置文字位置/内容/颜色/字体
        elif len(words) <= 12:
            draw.text((80, 600), words, (0, 0, 0), font=self.set_font(50))    #设置文字位置/内容/颜色/字体
        else:
            words1 = words[:12]   
            words2 = words[12:]   
            draw.text((60, 600), words1, (0, 0, 0), font=self.set_font(40))    #设置文字位置/内容/颜色/字体
            draw.text((60, 640), words2, (0, 0, 0), font=self.set_font(40))    #设置文字位置/内容/颜色/字体
        draw = ImageDraw.Draw(im1)                          #Just draw it!
        #im1.show()
        #另存图
        im1.save("material/target.jpg")

if __name__ == "__main__":
    words = u'哈哈哈'
    pic_num = 1
    make_pic = Make_express().make_pic(words,pic_num)
