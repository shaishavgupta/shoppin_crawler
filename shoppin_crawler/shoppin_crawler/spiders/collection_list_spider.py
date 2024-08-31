import scrapy

class CollectionListSpider(scrapy.Spider):
    name = 'collection_list_spider'
    start_urls = [
        'https://www.urbanmonkey.com',
    ]

    # this can be a regex or llm calls
    def is_catalog_link(self, link:str) -> bool:
        return 'collection' in link

    def parse(self, response, **kwargs):
        links = response.css('a::attr(href)').getall()
        filtered_links = [link for link in links if self.is_catalog_link(link)]

        # Yield the filtered links
        for link in filtered_links:
            yield {'link': response.urljoin(link)}