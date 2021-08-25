# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def change_url(value):
    try:
        result = value.replace('_s', '_b')
        return result
    except Exception:
        return value


def clear(value):
    try:
        result = value.replace(' ', ' ').replace('\n', '')
        return result
    except Exception:
        return value


class FotolmruItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=MapCompose(clear), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(change_url))
    link = scrapy.Field()


class JobparserItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    min = scrapy.Field()
    max = scrapy.Field()
    currency = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()


class HhruItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    min = scrapy.Field()
    max = scrapy.Field()
    currency = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()


class SjruItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    min = scrapy.Field()
    max = scrapy.Field()
    currency = scrapy.Field()
    website = scrapy.Field()
    link = scrapy.Field()
    _id = scrapy.Field()
