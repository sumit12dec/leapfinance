from scrapyscript import Job, Processor
from scrapy.spiders import Spider
from scrapy import Request
import json

from scrapy.crawler import CrawlerProcess
from extractor.spiders.myspider import GenericSpider

import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Pipe
from twisted.internet import reactor


def start_to_crawl(request_url, url_id):
    runner = crawler.CrawlerRunner()
    runner.crawl(GenericSpider, myurl=request_url, url_id=url_id)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()


def lp_entry_lambda(event, context=None):
    """used to predict based on the entry event from geospark backend
    """
    # NOTE assuming the event data is json already
    # from lxml import etree
    # print(__name__)

    # print(etree.LXML_VERSION)
    parent_connections = []
    processes = []

    response = 'N/A'
    print("lp_entry_lambda: ", event)
    a = 'None'
    if event.get("request_url"):
        print(event.get("request_url", "URL Not Found"))
        request_url = event.get("request_url")
        url_id = event.get("url_id")

        parent_conn, child_conn = Pipe()
        parent_connections.append(parent_conn)
        process = Process(target=start_to_crawl, args=(request_url, url_id,))
        processes.append(process)
        
        for process in processes:
            process.start()

        # make sure that all processes have finished
        for process in processes:
            process.join()

        # a = start_to_crawl(request_url=request_url, url_id=url_id)
    # print("fetching", a)
    return a


# if __name__ == '__main__':
#     lp_entry_lambda({"request_url": "https://lodgiq.com", "url_id": 1122})
