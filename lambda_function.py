import json


import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Pipe
from twisted.internet import reactor


from extractor.spiders.myspider import GenericSpider

def start_to_crawl(request_url, url_id):
    """Helper method to swapping crawling"""
    
    runner = crawler.CrawlerRunner()
    runner.crawl(GenericSpider, myurl=request_url, url_id=url_id)
    
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    
    reactor.run()


def lp_entry_lambda(event, context=None):
    """Entry point for lambda function
    """

    parent_connections = []
    processes = []

    response = 'N/A'
    a = 'None'

    if event.get("request_url"):
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

    return a


# if __name__ == '__main__':
#     lp_entry_lambda({"request_url": "https://lodgiq.com", "url_id": 1122})
