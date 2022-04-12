# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy_djangoitem import DjangoItem
from News.main.models import Article, NewsSite



class NewsSiteItem(DjangoItem):
    django_model = NewsSite


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    date_modified = scrapy.Field()
    date_published = scrapy.Field()
    id = scrapy.Field()
    image_src = scrapy.Field()






