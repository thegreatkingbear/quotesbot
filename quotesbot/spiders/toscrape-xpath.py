# -*- coding: utf-8 -*-
import scrapy
from quotesbot.items import QuoteItem, AuthorItem

class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath.py'
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            item = QuoteItem()
            item['text'] = quote.xpath('./span[@class="text"]/text()').extract()
            item['tags'] = quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            print("*" * 100)
            request = scrapy.Request(response.urljoin(quote.xpath('./span[2]/a/@href').extract_first()), callback=self.parseAbout)
            # pass item by embedding in the request as meta data
            request.meta['item'] = item
            print("request : ", request)
            yield request

        # sometimes it confuses me whether the extractions might be a list or not
        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            print("next page url :", next_page_url)
            request = scrapy.Request(response.urljoin(next_page_url))
            yield request

    def parseAbout(self, response):
        item = response.meta['item']
        author = AuthorItem()
        author['name'] = response.xpath('.//div[@class="author-details"]/h3/text()').extract_first()
        author['born'] = response.xpath('.//span[@class="author-born-date"]/text()').extract() + response.xpath('.//span[@class="author-born-location"]/text()').extract()
        author['description'] = response.xpath('.//div[@class="author-description"]/text()').extract_first()
        item['author'] = author
        yield item