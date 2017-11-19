# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

class Test1Spider(scrapy.Spider):
    name = 'test1'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com/S/JT']


    def parse(self, response):
        # ss = response.xpath('//table[@class="quote-info"]//tr')
        # print ss
        # print 'ssssssssssssssssssssss'
        # for sss in ss:
        #     print 'ssssssss'
        #     print sss
        item = {}
        # item['official_website'] = response.xpath('//div[@class="profile-detail hide"]/a/@href').extract_first()
        # tel = scrapy.Field()
        # addr = scrapy.Field()
        # item['introduction'] = response.xpath('//div[@class="profile-detail hide"]/text()')
        # official_website = scrapy.Field()
        item['introduction'] = response.xpath('//div[@class="profile-detail hide"]/text()').extract_first()
        item['official_website'] = response.xpath('//div[@class="profile-detail hide"]/a[1]/@href').extract_first()
        try:
            item ['addr'] = response.xpath('//div[@class="profile-detail hide"]/text()').extract()[1]
        except:
            item['addr'] = None
        item['tel'] = response.xpath('//div[@class="profile-detail hide"]/text()').extract()[-1]
        item['document'] = response.xpath('//div[@class="profile-detail hide"]/a[2]/@href').extract_first()
        print item