from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.scraper.spiders.spiders import TheEconomistQ2


def run_spider():
    def handle(self, *args, **kwargs):
        process = CrawlerProcess(get_project_settings())

        process.crawl(TheEconomistQ2)
        process.start()

