from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from scraper.scraper.spiders.spiders import TheEconomistQ2


def run_spider():
    configure_logging()
    runner = CrawlerRunner()
    task = LoopingCall(lambda: runner.crawl(TheEconomistQ2))
    task.start(60*30)
    reactor.run()


