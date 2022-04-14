import scrapy
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import XMLFeedSpider
from ..items import ArticleItem, NewsSiteItem
from News.main.models import NewsSite
import scrapy
import logging
import time
from scrapy import signals, Request
from w3lib.html import remove_tags

class NewsSiteSpider(scrapy.Spider):
    name = ""

    start_urls = [
        'https://www.economist.com/sitemap-2022-Q2.xml',
    ]

    def parse(self, response):
        filename = 'news.txt'
        with open(filename, 'wb') as f:
            f.truncate()
            f.write(response.body)


class TheEconomistQ2(XMLFeedSpider):
    name = "economist"
    allowed_domains = ["www.economist.com"]
    start_urls = [
        'https://www.economist.com/sitemap-2022-Q2.xml',
    ]

    namespaces = [('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')]
    itertag = 'n:loc'
    iterator = 'xml'

    name_path = ".//urlset/url/loc/text()"


    def parse_node(self, response, node):
        urls = node.xpath("./text()").extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_attr)

    def parse_attr(self, response):
        title = "".join(response.css('.article__headline::text').getall())
        if title == "":
            title = "".join(response.css('.css-1bo5zl0::text').getall())

        with_tags = "".join(response.css('p.article__body-text').getall())
        clean_text = remove_tags(with_tags)
        content = clean_text
        url = response.url
        date_modified = "".join(response.css(".article > meta:nth-child(6)::attr(content)").getall(), )
        date_published = "".join(response.css(".article > meta:nth-child(7)::attr(content)").getall(), )
        id = int(1)
        image = response.css(".article__lead-image > div:nth-child(1) > meta:nth-child(1)::attr(content)").get()
        item = ArticleItem(title=title, content=content, url=url, date_modified=date_modified,
                           date_published=date_published, id=id, image_src=image)
        yield item


# class DeutscheWelle(XMLFeedSpider):
#     name = "DW"
#     allowed_domains = ["www.dw.com"]
#     start_urls = [
#         'https://www.dw.com/en/news-sitemap.xml',
#     ]
#
#     namespaces = [('n', 'http://www.sitemaps.org/schemas/sitemap/0.9')]
#     itertag = 'n:loc'
#     iterator = 'xml'
#
#     name_path = ".//urlset/url/loc/text()"
#
#
#     def parse_node(self, response, node):
#         urls = node.xpath("./text()").extract()
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse_attr)
#
#     def parse_attr(self, response):
#         title = str(response.css("head > meta:nth-child(115)::attr(content)").get()).split(" | ")[0]
#         content = "".join(response.css('.longText > p::text').getall(), )
#         url = response.url
#         date_published = str((response.css("head > meta:nth-child(115)::attr(content)").get())).split(" | ")[2]
#         date_modified = str((response.css("head > meta:nth-child(115)::attr(content)").get())).split(" | ")[2]
#         id = int(2)
#         image = response.css(".article__lead-image > div:nth-child(1) > img:nth-child(2)::attr(src").get()
#
#         item = ArticleItem(title=title, content=content, url=url, date_modified=date_modified, date_published=date_published, id=id, image=image)
#         yield item
#
