# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MajorinfospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #学校名
    school_name = scrapy.Field()
    #学校主页链接
    school_url = scrapy.Field()
    #学校id
    school_id = scrapy.Field()
    #学校专业详细页链接
    major_url = scrapy.Field()
    #专业信息列表 例:{'经济学':['产业经济','农林经济','政府经济'],'工学':['电子信息','计算机']}
    major_info = scrapy.Field()