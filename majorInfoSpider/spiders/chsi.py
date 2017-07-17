# -*- coding: utf-8 -*-
import scrapy
import sys
import json
from majorInfoSpider.items import MajorinfospiderItem
reload(sys)
sys.setdefaultencoding('utf-8')
class ChsiSpider(scrapy.Spider):
    name = "chsi"
    allowed_domains = ["gaokao.chsi.com.cn"]
    start_urls = (
        'http://gaokao.chsi.com.cn/sch/search--ss-on,option-qg,searchType-1.dhtml',
    )

    def parse(self, response):
        #获取下一页链接,并请求(需要判断是否是最后一页面)
        next_urls = response.xpath('//*[@id="PageForm"]//li[last()]/a/@href').extract()
        if len(next_urls) != 0:
            yield scrapy.Request(next_urls[0],callback=self.parse)
        #获取当前页学校名称列表
        school_names = response.xpath('//table[2]//a/text()').extract()
        #获取当前页学校主页链接列表
        school_urls = response.xpath('//table[2]//a/@href').extract()
        #循环遍历school_names.school_urls,将学校名\学校id\学校主页链接保存
        for school_name,school_url in zip(school_names,school_urls):
            school_url = 'http://gaokao.chsi.com.cn' + school_url
            item = MajorinfospiderItem()
            item['school_name'] = school_name
            item['school_url'] = school_url
            item['school_id'] = school_url.split('-')[3].split('.')[0]
            print '%s--'%item['school_id'] * 30
            #请求学校主页页面,回调parse_main_page解析结果
            yield scrapy.Request(school_url,meta={'item':item},callback=self.parse_main_page)
    #解析学校主页,请求专业详细页地址
    def parse_main_page(self,response):
        item = response.meta['item']
        major_url = 'http://gaokao.chsi.com.cn' + response.xpath('//div[@class="r_c_box"][2]//span[1]/a/@href').extract()[0]
        item['major_url'] = major_url
        #请求本学校专业更多链接,进入专业详细页面
        yield scrapy.Request(major_url,meta={'item':item},callback=self.parse_major_page)
    #解析专业详细页,保存到item,并yielditem
    def parse_major_page(self,response):
        item = response.meta['item']
        all_major_dict = {}
        major_names = response.xpath('//li[@class="r_zyjs_type"]/text()').extract()
        major_details = response.xpath('//li[@class="r_zyjs_majors"]')
        for major_name,major_detail in zip(major_names,major_details):
            major_detail = major_detail.xpath('.//a/text()|.//span/text()').extract()
            all_major_dict[major_name.strip()] = [major for major in [major.strip() for major in major_detail] if major != ""]
        item['major_info'] = all_major_dict
        yield item
