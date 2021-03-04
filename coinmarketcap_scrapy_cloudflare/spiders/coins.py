# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_cloudflare_middleware.middlewares import CloudFlareMiddleware

class CoinsSpider(CrawlSpider):
    name = 'coins'
    allowed_domains = ['coinmarketcap.com']
    start_urls = ['https://coinmarketcap.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td/a[@class='cmc-link']", unique=True), callback='parse_item', follow=True),
    )


    def remove_characters(self, value):
        return value.strip(' Price')

    def parse_item(self, response):
        yield {
            'name': self.remove_characters(response.xpath("//h1[starts-with(@class, 'priceHeading')]/text()").get()),
            'rank': response.xpath("//div[@class='namePill___3p_Ii namePillPrimary___2-GWA']/text()").get(),
            'price': response.xpath("//div[@class='priceValue___11gHJ']/text()").get()
            }