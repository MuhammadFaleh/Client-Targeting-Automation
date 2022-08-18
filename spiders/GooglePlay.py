import json
import requests
import scrapy
from dateutil.relativedelta import relativedelta
from scrapy.loader import ItemLoader
from items import GooglePlayItem
from unidecode import unidecode
from datetime import datetime
import pandas as pd


class GooglePlay(scrapy.Spider):
    name = 'Gp_scraper'

    def start_requests(self):
        data = pd.read_csv("Maroof.csv", usecols=['Android'])
        data = data[data['Android'].notna()]
        data = data[data.values != 'None']
        link_list = data.values.tolist()
        link_list = sum(link_list, [])
        self.urls = link_list
        for url in self.urls:
            yield scrapy.Request(url, callback=self.parse, method='GET')

    def parse(self, response):
        item = ItemLoader(item=GooglePlayItem(), selector=response)
        item.add_value('url', response.request.url)
        item.add_xpath('downloads', "//div[@class='ClM7O']/text()")
        item.add_xpath('reviews', "//div[@class='g1rdde']/text()")
        item.add_xpath('score', "//div[@class='TT9eCd']/text()")
        item.add_xpath('last_patch', "//div[@class='xg1aie']/text()")
        yield item.load_item()
