# -*- coding: utf-8 -*-
from xueqiu.items import XueqiuItem
import scrapy
import time
import json


class SummarizedSpider(scrapy.Spider):
    name = 'summarized'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com']
    url_list = ['https://xueqiu.com/stock/quote.json?code=HKHSI%2CHKHSCCI%2CHKHSCEI%2CHKVHSI&_=',
                'https://xueqiu.com/stock/quote.json?code=DJI30%2CQQQ%2CSP500%2CICS30&_=',
                'https://xueqiu.com/stock/quote.json?code=SH000001%2CSZ399001%2CSH000300%2CSZ399006&_=',
                'https://xueqiu.com/stock/quote.json?code=SH000011%2CSZ399305&_=',
                'https://xueqiu.com/stock/quote.json?code=BITSTAMPUSD%2CBTCEUSD%2CBTCNCNY%2CBTCDEEUR&_=',
                'https://xueqiu.com/stock/quote.json?code=TF1403.FM%2CTF1406.FM&_='
                ]


    def parse(self, response):
        for url in self.url_list:
            url = url + str(int(time.time()) * 1000)
            yield scrapy.Request(url=url, callback=self.parse_data)

    def parse_data(self,response):
        data_list = json.loads(response.body)["quotes"]
        for data in data_list:
            item = XueqiuItem()
            item["symbol"] = data['symbol']
            item["exchange"] = data['exchange']
            item["code"] = data["code"]
            item["name"] = data['name']
            item["current"] = data['current']
            item["percentage"] = data['percentage']
            item["change"] = data['change']
            item["open"] = data['open']
            item["high"] = data['high']
            item["low"] = data['low']
            item["close"] = data['close']
            item["last_close"] = data['last_close']
            item["high52week"] = data['high52week']
            item["low52week"] = data['low52week']
            try:
                item['rise_count'] = data['rise_count']
            except:
                item['rise_count'] = 0
            try:
                item['flat_count'] = data['flat_count']
            except:
                item['flat_count'] =0
            try:
                item['fall_count'] = data['fall_count']
            except:
                item['fall_count'] = 0
            item['marketCapital'] = data['marketCapital']
            item['market_status'] = data['market_status']
            item['lot_volume'] = data['lot_volume']
            item['amount'] = data['amount']
            item['currency_unit'] = data['currency_unit']
            item['rise_stop'] = data['rise_stop']
            item['fall_stop'] = data['fall_stop']
            item['beta'] = data['beta']

            yield item

