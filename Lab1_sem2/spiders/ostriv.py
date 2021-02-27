# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class OstrivSpider(scrapy.Spider):
    name = 'ostriv'
    allowed_domains = ['tsikave.ostriv.in.ua']
    start_urls = ['http://tsikave.ostriv.in.ua/']

    def parse(self, response: Response):
        all_images = response.xpath("//article/a/img/@src")
        all_text = response.xpath("//*[not(self::script)][not(self::style)][string-length(normalize-space(text())) > 30]/text()")
        yield {
            'url': response.url,
            'payload': [{'type': 'text', 'data': text.get().strip()} for text in all_text] +
                       [{'type': 'image', 'data': 'http://tsikave.ostriv.in.ua' + image.get()[22:len(image.get())-2]} for image in all_images]
        }
        if response.url == self.start_urls[0]:
            all_links = response.xpath(
                "//a/@href[starts-with(., '/list/')]")
            selected_links = ['http://tsikave.ostriv.in.ua' + link.get() for link in all_links][:19]
            for link in selected_links:
                yield scrapy.Request(link, self.parse)
