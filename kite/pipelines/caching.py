# -*- coding: utf-8 -*-
# @Time    : 2021/1/17 14:57:30
# @Author  : sunnysab
# @File    : caching.py

import scrapy
from scrapy.pipelines.files import FilesPipeline

from kite.items import StoreItem


class FileCachingPipeline(FilesPipeline):
    """
    Write files into disk cache, based on FilesPipeline in scrapy.
    """

    def get_media_requests(self, item: StoreItem, info):
        if not item['is_continuing']:
            return []

        yield scrapy.Request(item['url'], meta={'title': item['title']})

    def item_completed(self, results, item: StoreItem, info):
        for b_result, result_info in results:
            if not b_result:
                item['is_continuing'] = False
            else:
                item['is_continuing'] = True
                item['checksum'] = result_info['checksum']
                item['path'] = result_info['path']

            return item
