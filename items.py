# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
from urllib.parse import urlparse
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
import scrapy


def remove_space(value):
    return str(value).strip()


def replace_mail(value):
    return value.replace("mailto:", "")


def fix_url(value):
    if not re.match('(?:http|ftp|https)://', value) and value is not None:
        value = 'http://' + value
    obj = urlparse(value)
    value = 'http://{}'.format(obj.netloc)
    if re.match('(?:..|/..)', value):
        value = value.replace('..', '.')
    return value

# any operations on data such as cleaning are meant to be here


class MarofItem(scrapy.Item):
    # Main Info:
    Url = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    Name = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    Rating = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    Ratters = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    IOS = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    Activity = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    ResComments = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    CRNumber = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    # contact Info:
    Twitter = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    count = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    Insta = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    Phone = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    Email = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    Whatsapp = scrapy.Field(input_processor=MapCompose(fix_url), output_processor=TakeFirst())
    #

    Website = scrapy.Field(input_processor=MapCompose(fix_url), output_processor=TakeFirst())
    Location = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    Android = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())


class WebsiteItem(scrapy.Item):
    Website = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    ECommerce = scrapy.Field()


class GooglePlayItem(scrapy.Item):
    downloads = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    reviews = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    score = scrapy.Field(input_processor=MapCompose(remove_space), output_processor=TakeFirst())
    last_patch = scrapy.Field(input_processor=MapCompose(remove_space))
    Android = scrapy.Field(input_processor=MapCompose(remove_space))
