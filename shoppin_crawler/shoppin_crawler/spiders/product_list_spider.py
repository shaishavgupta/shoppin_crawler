import urllib
import scrapy
from scrapy_splash import SplashRequest


class ProductListSpider(scrapy.Spider):
    name = 'product_list_spider'

    def __init__(self):
        self.all_urls = []
        self.pagination_funcs = [self.get_cursor_query_param_pagination, self.get_limit_offset_based_paginations]
        self.previous_filtered_products = []

    def start_requests(self):
        start_urls = ['https://www.urbanmonkey.com/collections/new-arrivals']
        for url in start_urls:
            for pagination_func in self.pagination_funcs:
                yield SplashRequest(url=pagination_func(url), callback=self.parse)

    # this can be a regex or llm calls
    def is_product_link(self, link:str) -> bool:
        return 'products/' in link


    def parse(self, response, **kwargs):
        links = response.css('a::attr(href)').getall()
        
        # Join relative URLs with the base URL
        filtered_products = [link for link in links if self.is_product_link(link)]
        has_products = len(filtered_products) > 0

        # Yield the filtered links
        for link in filtered_products:
            yield {'link': response.urljoin(link)}
        if has_products and filtered_products not in self.previous_filtered_products:
            yield SplashRequest(url=self.get_next_page_url(response.url), callback=self.parse)
        self.previous_filtered_products.append(filtered_products)


    def get_cursor_query_param_pagination(self, url):
        return f'{url}?page=1'
    
    def get_limit_offset_based_paginations(self, url):
        return f'{url}?limit=10&offset=0'
    
    def get_next_page_url(self, url:str):
        base_url = ''.join(url.split('?')[:-1])
        if '?page=' in url:
            current_page = int(url.split('page=')[-1])
            return f'{base_url}?page={current_page+1}'

        elif 'limit=' in url and 'offset=' in url:
            params = url.split('?')[-1]
            query_params = params.split('&')
            
            current_limit = int(query_params[0].split('limit=')[-1])
            current_offset = int(query_params[1].split('offset=')[-1])
            
            return f'{base_url}?limit={current_limit}&offset={current_offset+current_limit}'
