from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from scraper.scraper.spiders.spiders import TheEconomistQ2
from crochet import setup
from scraper.scraper import settings as my_settings

def run_spider():
    crawler_settings = Settings()
    setup()
    configure_logging()
    runner = CrawlerRunner()
    crawler_settings.setmodule(my_settings)
    task = LoopingCall(lambda: runner.crawl(TheEconomistQ2))
    task.start(60*30)
    reactor.run()