import scrapy
from itemloaders import ItemLoader
from scrapy.selector import Selector
from scrapy import Request
from urllib.parse import urlparse
import pandas as pd
from items import WebsiteItem


class CheckWebSpider(scrapy.Spider):
    name = 'website_spider'

    def start_requests(self):
        data = pd.read_csv("Maroof.csv", usecols=['Website'])
        data = data[data['Website'].notna()]
        data = data[data.values != 'None']
        link_list = data.values.tolist()
        link_list = sum(link_list, [])
        for link in link_list:
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response, **kwargs):
        if int(response.xpath("boolean(//link[contains(@href, 'https://media.zid.store')])").get()) == 1:
            Ecom = "zid"
        elif int(response.xpath("boolean(//body[contains(@class, 'store-home salla')])").get()) == 1:
            Ecom = "salla"
        else:
            Ecom = "None"

        item = ItemLoader(item=WebsiteItem(), selector=response)
        item.add_value('ECommerce', Ecom)
        item.add_value('Website', response.request.url)

        yield item.load_item()
