# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
from pathlib import Path
from datetime import datetime
from scrapy.exporters import CsvItemExporter

class VikkaPipeline:
    def process_item(self, item, spider):
        return item


# class SaveToCSVPipeline(object):
#     report_filename = '123' #как то вытащить дату с spider
#     fields_to_export_news = []
#     # report_filename = ''
#
#     # at startup
#     def open_spider(self, spider):
#         self.file = None
#
#     # at finish spider work
#     def close_spider(self, spider):
#         if self.file:
#             self.file.close()
#
#     def process_item(self, item, spider):
#         if not self.file:
#             self.init_exporter(Path(__file__).parent.parent / 'news')
#         self.exporter_url.export_item(item)
#         return item
#
#     def init_exporter(self, report_path):
#         if not os.path.isdir(report_path):
#             os.makedirs(report_path)
#         filename = os.path.join(report_path, f'{self.report_filename}.csv')
#         self.file = open(filename, 'wb')
#         self.exporter_url = CsvItemExporter(self.file, fields_to_export=self.fields_to_export_news)
#
#     def user_date(self):
#         pass

