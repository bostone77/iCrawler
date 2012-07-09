#coding: utf-8
'''
Created on 2012-2-9

@author: joyce
'''
import re
import time
from pyquery import PyQuery
import Image
import string

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = '27_tg'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        
        
        item = ContentItem() 
        content_image = doc('div#team_images').find('img').attr('src')
        item['pic_url'] = content_image
        
        content = doc('div#team_main_side')+doc('div#side-business')
        content.remove('div[style = "margin-top:10px;"]')
        
        
        imgs = content('img')
        img_all = []
        for img in imgs:
            if".gif" in img.get('src'):
                continue
            if".GIF" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all

        item['title'] = self.title = doc('div#deal-intro').find('h1').text()
        item['content'] = self.content = self.title + content.__unicode__()
        item['release_time'] = ''
#        item['release_switch_time'] = self.release_switch_time = time.time()
        item['source'] = u"爱丽"
        item['author'] = ''
        
        deadline_s=time.time()
        deadline_d = doc('div[class = "deal-timeleft deal-on"]').attr('diff')
        deadline_d = deadline_d[0:6]
        deadline_d = string.atoi(deadline_d)
        deadline = deadline_s + deadline_d
        deadline = time.localtime(deadline)
        item['deadline'] = time.strftime('%Y-%m-%d',deadline)
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
