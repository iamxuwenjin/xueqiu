# -*- coding: utf-8 -*-
import json
import time
import scrapy
from xueqiu.items import UsNewStock


class UsNewStockSpider(scrapy.Spider):
    name = 'us_new_stock'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com']
    base_url = "https://xueqiu.com/S/"
    page_num = 1
    url = 'https://xueqiu.com/stock/ipo_listed_us.json?page='+str(page_num)+'&size=90&order=desc&orderBy=ipo_date&_='

    def parse(self, response):
        url = self.url + str(int(time.time()) * 1000)
        yield scrapy.Request(url=url, callback=self.parse_data)

    def parse_data(self,response):
        data_list = json.loads(response.body)["data"]
        for data in data_list:
            item = UsNewStock()
            item['symbol'] = data['symbol']
            item['company_name'] = data['company_name']
            item['ipo_date'] = data['ipo_date']
            item['shares'] = data['shares']
            item['ipo_price'] = data['ipo_price']
            item['close'] = data['close']
            item['chg'] = data['chg']
            item['percent'] = data['percent']
            url = self.base_url+item['symbol']
            yield scrapy.Request(url=url,meta={'item':item},callback=self.parse_detail)

    def parse_detail(self,response):
        item = response.meta['item']
        item['open'] = response.xpath('//table[@class="quote-info"]//tr[1]/td[1]/span/text()').extract_first()
        item['high'] = response.xpath('//table[@class="quote-info"]//tr[1]/td[2]/span/text()').extract_first()
        item['high52week'] = response.xpath('//table[@class="quote-info"]//tr[1]/td[3]/span/text()').extract_first()
        item['lot_volume'] = response.xpath('//table[@class="quote-info"]//tr[1]/td[4]/span/text()').extract_first()
        item['last_close'] = response.xpath('//table[@class="quote-info"]//tr[2]/td[1]/span/text()').extract_first()
        item['low'] = response.xpath('//table[@class="quote-info"]//tr[2]/td[2]/span/text()').extract_first()
        item['low52week'] = response.xpath('//table[@class="quote-info"]//tr[2]/td[3]/span/text()').extract_first()
        item['amplitude'] = response.xpath('//table[@class="quote-info"]//tr[2]/td[4]/span/text()').extract_first()
        item['turnover_rate'] = response.xpath('//table[@class="quote-info"]//tr[3]/td[1]/span/text()').extract_first()
        item['marketCapital'] = response.xpath('//table[@class="quote-info"]//tr[3]/td[2]/span/text()').extract_first()
        item['totalShares'] = response.xpath('//table[@class="quote-info"]//tr[4]/td[2]/span/text()').extract_first()
        text = response.xpath('//div[@class="profile-detail hide"]').extract_first()
        if text :
            item['introduction'] = response.xpath('//div[@class="profile-detail hide"]/text()').extract_first()
            item['official_website'] = response.xpath('//div[@class="profile-detail hide"]/a[1]/@href').extract_first()
            item['document'] = response.xpath('//div[@class="profile-detail hide"]/a[2]/@href').extract_first()
        yield item
        self.page_num +=1
        if self.page_num <= 9:
            url = self.url + str(int(time.time()) * 1000)
            yield scrapy.Request(url=url,callback=self.parse_data)

