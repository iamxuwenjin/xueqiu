# -*- coding: utf-8 -*-
import json
import time
import scrapy
from xueqiu.items import ShNewStock


class ShNewStockSpider(scrapy.Spider):
    name = 'sh_new_stock'
    allowed_domains = ['xueqiu.com']
    start_urls = ['https://xueqiu.com/']
    page_num = 1
    url = 'https://xueqiu.com/proipo/query.json?page='+str(page_num)+'&size=90&order=desc&orderBy=list_date&stockType=&column=symbol%2Cname%2Conl_subcode%2Clist_date%2Cactissqty%2Conl_actissqty%2Conl_submaxqty%2Conl_subbegdate%2Conl_unfrozendate%2Conl_refunddate%2Ciss_price%2Conl_frozenamt%2Conl_lotwinrt%2Conl_lorwincode%2Conl_lotwiner_stpub_date%2Conl_effsubqty%2Conl_effsubnum%2Conl_onversubrt%2Coffl_lotwinrt%2Coffl_effsubqty%2Coffl_planum%2Coffl_oversubrt%2Cnapsaft%2Ceps_dilutedaft%2Cleaduwer%2Clist_recomer%2Cacttotraiseamt%2Conl_rdshowweb%2Conl_rdshowbegdate%2Conl_distrdate%2Conl_drawlotsdate%2Cfirst_open_price%2Cfirst_close_price%2Cfirst_percent%2Cfirst_turnrate%2Cstock_income%2Conl_lotwin_amount%2Clisted_percent%2Ccurrent%2Cpe_ttm%2Cpb%2Cpercent%2Chasexist&type=quote&_='
    def parse(self, response):
        url = self.url + str(int(time.time()) * 1000)
        yield scrapy.Request(url=url, callback=self.parse_data)

    def parse_data(self,response):
        column_list = json.loads(response.body)['column']
        data_list = json.loads(response.body)["data"]
        # data_list是data列表的大列表
        for data in data_list:
            item = ShNewStock()
            for column,data_info in zip(column_list,data):
                item[column]= data_info
            yield item
        self.page_num += 1
        if self.page_num <= 40:
            url = self.url + str(int(time.time()) * 1000)
            yield scrapy.Request(url=url, callback=self.parse_data)


