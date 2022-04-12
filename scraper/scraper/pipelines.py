# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from News.main.models import NewsSite, Article
from django.db import transaction


class ScraperPipeline:
    def process_item(self, item, spider):
        return item


class BotsPipeline(object):
    def process_item(self, item, spider):
        try:
            news_site = NewsSite.objects.get(pk=item["id"])
            if item["title"] == "" or item["content"] == "":
                return item
            try:
                a = Article.objects.get(title=item["title"])
                if a.content == item["content"]:
                    return item
                a.content = item["content"]
                a.date_modified = item["date_modified"]
            except:
                article = Article(None, item["title"], item["url"], item["content"], news_site, item["date_modified"], item["date_published"], item["image_src"])
                article.save()
                return item
        except:
            news_site = NewsSite.objects.get(pk=item["id"])
            if item["title"] == "" or item["content"] == "":
                return item
            try:
                a = Article.objects.get(title=item["title"])
                if a.content == item["content"]:
                    return item
                a.content = item["content"]
                a.date_modified = item["date_modified"]
            except:
                article = Article(None, item["title"], item["url"], item["content"], item["id"], item["date_modified"], item["date_published"], item["image_src"])
                article.save()
                return item

