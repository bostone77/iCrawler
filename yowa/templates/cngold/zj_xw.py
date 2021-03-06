#coding: utf-8

import re
import time
from pyquery import PyQuery
import Image

from yowa.templates.BaseTemplate import Base
from yowa.items import ContentItem

class Parser(Base):
    name = 'zj_cngold'

    def extract(self):
        self.html = re.sub('<!--.*?-->', '', self.html)
        doc = PyQuery(self.html)
        content_node = doc('div.det_content')
        content_node.remove('div.det_read')
        content_node.remove('div.in_content_left_advs')
        content_node.remove('iframe')
        content_node.remove('script')
        
        item = ContentItem()
        imgs = content_node('img')
        img_all = []
        for img in imgs:
            if ".gif" in img.get('src'):
                continue
            else:  
                imgs.eq(imgs.index(img)).append('<br>')
                imgs.eq(imgs.index(img)).before('<br>')
                img_all.append(self.getRealURI(img.get('src')))
        item['image_urls'] = img_all
        
        self.title = doc('h1').text()
        item['title'] = self.title
        item['content'] = self.content = content_node.__unicode__()
        release_time=doc('div.det_title').text()
        r = re.compile(u"(20\d\d-.*\d\d:\d\d)")
        self.release_time = r.search(release_time).group()
        item['release_time'] = self.release_time
#        item['release_switch_time'] = self.release_switch_time = time.mktime(time.strptime(release_time,u'%Y��%m��%d��%H:%M'))
        item['source'] = u"中国黄金投资网"
        item['author'] = ''
        item['pic_url'] = ''
        
        return item

    def isMatch(self, ):
        if len(self.title) > 0 and len(self.content) > 0:
            return True
        else:
            return False
