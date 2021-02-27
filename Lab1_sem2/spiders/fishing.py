# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class FishingSpider(scrapy.Spider):
    name = 'fishing'
    allowed_domains = ['fishing-mart.com.ua']
    start_urls = ['http://www.fishing-mart.com.ua/2-fishing-mart-spinningovaya-ribalka?id_category=2&n=60']

    def parse(self, response: Response):
        products = response.xpath("//div[contains(@class, 'product-container')]")[:20]
        for product in products:
            yield {
                'description': product.xpath(".//img[@class='replace-2x img-responsive']/@title").get(),
                'price': product.xpath(".//span[@class='price product-price']/text()").get(),
                'img': product.xpath(".//img[@class='replace-2x img-responsive']/@src").get()
            }