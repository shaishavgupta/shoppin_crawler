import threading
from fastapi import FastAPI
from shoppin_crawler.shoppin_crawler.spiders.collection_list_spider import CollectionListSpider
from shoppin_crawler.shoppin_crawler.spiders.product_list_spider import ProductListSpider
from helper import run_crawler, get_collection_urls
from constants import COLLECTION_URLS_FILE, PRODUCT_URLS_FILE
from scrapy.crawler import CrawlerRunner
from scrapy import signals
from scrapy.signalmanager import dispatcher
from twisted.internet import reactor, defer


app = FastAPI()

@app.get("/get-collections")
async def get_collection_urls():
    # get collection urls
    run_crawler(CollectionListSpider, COLLECTION_URLS_FILE)
    thread = threading.Thread(target=run_crawler, args=(CollectionListSpider, COLLECTION_URLS_FILE))
    thread.start()
    thread.join()

    # # validate and get collection urls from json
    # urls = await get_collection_urls()
    
    return {"success": True}

@app.get("/get-products")
async def get_product_urls():
    # get product urls
    thread = threading.Thread(target=run_crawler, args=(ProductListSpider, PRODUCT_URLS_FILE))
    thread.start()
    thread.join()
    
    return {"success": True}
