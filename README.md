# shoppin_crawler

> [!TIP]
> Using FastApi but Sanic is faster as per benchmarks.

## Problem Statement
### Statement
> Design and implement a web crawler whose primary task is to discover and list all product URLs across multiple e-commerce websites. You will be provided with a list of domains belonging to various e-commerce platforms. The output should be a comprehensive list of product URLs found on each of the given websites.

### Input:
> A list of domains that belong to different e-commerce websites.
Example: [“example1.com”, “example2.com”, example3.com”…]
The crawler should be able to handle a minimum of 10 domains and scale to handle potentially hundreds.

### Output:
> A structured list or file that contains all the discovered product URLs for each domain. The output should map each domain to its corresponding list of product URLs.
The URLs should be unique and must point directly to product pages (e.g., www.example.com/product/12345).

### Key Features:

> 1. **⁠URL Discovery**: The crawler should intelligently discover product pages, considering different URL patterns that might be used by different websites (e.g., /product/, /item/, /p/).
> 2. **⁠Scalability**: The solution should be able to handle large websites with deep hierarchies and a large number of products efficiently.
> 3. **⁠Performance**: The crawler should be able to execute in parallel or asynchronously to minimize runtime, especially for large sites.
> 4. **⁠Robustness**: Handle edge cases such as: Websites with infinite scrolling or dynamically loaded content, Variations in URL structures across different e-commerce platforms.

## Some Clarification Questions

- what domains should i use as and example for reference as big companies like Flipkart does not allows you to parse their codebase.
- No need to solutions for blocking domains.
- will this be a async task or this will run on demand. -> async task
- what scale are we looking at.
- what should be the complete flow or just need to fetch the data from the websites -> using domain fetch all product urls
- what if the website we are crawling goes down or is not functional anymore. -> redo
- what if crawled product is updated from the source website we will be updating it from our website or we will add again and delete the old one. -> ignore this

</br>

> [!NOTE]
>  Ideally this should be a cron of some kind, because we might have a lot of domains to crawl with async jobs.

## Approaches
1. Map inventory apis along with list of all its products and find the pattern among them.
2. parse all the html content fetch all hrefs and identify if current href is a product link or not.
	- can be identified via patterns
		- product/, /item/, /p/.
	- can be identified via some ml algo.
	- can be identified via response.
		- will have common characterstics like resp will be of list, with a link.and price, name/display_name.
	- can be mapped in database.

### Went Ahead with Approach 2.
- We can parse the html, but html can have different links `inventory`, `products`, `seo`, `t&c` and we will find `inventory using regex` and will ignore rest all including product to avoid redundancy.
- **Problem is Inventory URL Identification**
    - Regex can be identified manually finding patterns or using fine tuned `llm models`.
- **Problem is Number of Links on a domain**
    - There can be a lot of different links but we cannot send them all as that will consume a lot of tokens hence will be expensive.
        - Assuming 10000 Links on each domain after dedupe we can reduce the number significantly
        - Some urls can be eliminated like t&c, about_us etc.
        - product urls or urls having ids in their path.
        - dedupe similar patterns and send only one among them.
            - eg:- `snitch.com/catalog/?item=shirts` and `snitch.com/catalog/?item=tanktops` can be collected and we can send only one among them.
    - with above assumptions and optimisations and `data cleaning` we can reduce the overall request to llm model significantly upto 95-99%.
- After we have successfully collected list of catalog urls, now its time to process them to get all products.
- Now using regex and llm models we can identify the correct way to fetch the product from the inventory we have.

- **Pagination and infinite scrolling**
    - As all the inventory urls are GET requests and can be paginated.
    - to solve this we will have to try out all the possible ways to paginate and find out the correct one being implemented by the current domain.
    - Upon identification we will keep on hitting the request until we get all the data if the current product.

- **LLM Hallucination Problem**
    - LLM's can easily hallucinate hence the data needs to be verified.
        - Sampling
        - using other llm for verification

## Future Scope and Improvements
> [!TIP]
> Pagination technique identifiaction can be altogether be broken into different microservice responsible for identifying the pagination method used by domain.

> [!TIP]
> We can have a microservice for validating the false +ves and false -ves from llm response to detect the trusworthiness of llm responses.

> [!TIP]
> We have to deduce a way to update the items in-stock and out-of-the stock and their quantities in realtime and update ourselves as well.

## Setting up

> [!NOTE]
> Using Python==3.9.19, fastapi==0.112.2, Scrapy==2.11.2, splash==3.5(for dynamic webpage crawling).

1. Cloning the repo.
2. Create Virtual Environment.`python -m venv venv`.
3. Activate it `source venv/bin/activate`
4. Install Required Dependencies `pip install -r requirements.txt`.
5. Start Server `fastapi run main.py`
6. starting splash `docker run -it -p 8050:8050 --rm scrapinghub/splash`

## Implementation Details
1. Starting up server exposes 2 endpoints
    1. `/get-collections` gets list of collections from the `start_urls` list in `collection_list_spide.py`.
    2. `/get-products` gets list of products from the `start_urls` in `start_requests` function in `product_list_spider.py`.
