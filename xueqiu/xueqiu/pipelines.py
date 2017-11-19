# -*- coding: utf-8 -*-

from scrapy.exporters import CsvItemExporter
from xueqiu.items import XueqiuItem,UsNewStock,ShNewStock
from datetime import datetime
import json

class XueqiuPipeline(object):
    def process_item(self, item, spider):
        item['utc_time'] = str(datetime.utcnow())
        return item

class XueqiuCSvPipeline(object):
    def open_spider(self,spider):
        self.filename = open('summarized.csv','w')
        self.csv_exporter = CsvItemExporter(self.filename)
        self.csv_exporter.start_exporting()

    def process_item(self,item,spider):
        if isinstance(item, XueqiuItem):
            self.csv_exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.csv_exporter.finish_exporting()
        self.filename.close()

class UsNewStockCSvPipeline(object):
    def open_spider(self,spider):
        self.filename = open('us_new_stock.csv','w')
        self.csv_exporter = CsvItemExporter(self.filename)
        self.csv_exporter.start_exporting()

    def process_item(self,item,spider):
        if isinstance(item, UsNewStock):
            self.csv_exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.csv_exporter.finish_exporting()
        self.filename.close()

class ShNewStockCSvPipeline(object):
    def open_spider(self,spider):
        self.filename = open('sh_new_stock.json','w')

    def process_item(self,item,spider):
        content = json.dumps(dict(item))
        if isinstance(item, ShNewStock):
            self.filename.write(content)
        return item

    def close_spider(self,spider):
        self.filename.close()

