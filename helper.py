import json
from scrapy.crawler import CrawlerProcess
from constants import COLLECTION_URLS_FILE

def run_crawler(spider_cls, output_filename):
    process = CrawlerProcess(settings={
        "FEEDS": {
            output_filename: {"format": "json"},
        },
    })

    process.crawl(spider_cls)
    process.start()
    process.stop()


async def read_json_file(filename):
    data = None
    with open(filename, 'r') as file:
        data = json.load(file)
    return data


async def write_json_file(filename, content):
    json_object = json.dumps({"data":content}, indent=4)

    with open(filename, 'w') as file:
        file.write(json_object)


async def validate_collection_urls(urls: set):
    patterns = {}
    for url in urls:
        url_pattern = str(url.split('/')[:-1])
        if not patterns.get(url_pattern):
            patterns[url_pattern] = []
        patterns[url_pattern].append(url)
    return patterns

async def get_collection_urls():
    urls = await read_json_file(COLLECTION_URLS_FILE)
    if not urls: 
        return []
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # validation of collection urls
    url_with_patterns = await validate_collection_urls(set([link['link'] for link in urls if link.get('link')]))
    valid_collection_urls = []

    for url_pattern in url_with_patterns.keys():
        if len(url_with_patterns[url_pattern]) < len(valid_collection_urls):
            valid_collection_urls = url_with_patterns[url_pattern]

    # return pattern with most similar patterns
    return valid_collection_urls

