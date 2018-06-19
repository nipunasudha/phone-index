# -*- coding: utf-8 -*-
import unicodedata

import scrapy


class PhoneSpider(scrapy.Spider):
    name = 'phone'
    api_url = 'https://www.phonearena.com/phones/page/{}'

    start_urls = [api_url.format(1)]

    def parse(self, response):
        phone_urls = response.css('a.s_thumb::attr(href)').extract()
        for phone_url in phone_urls :
            yield scrapy.Request(url=response.urljoin(phone_url), callback=self.parse_details)
        p = response.url.split('/')[-1]
        yield scrapy.Request(url=self.api_url.format(int(p) + 1), callback=self.parse)


    def parse_details(self, response):
        morespecs = response.css('div.morespecs')


        yield {
            'name': self.preprocess(response.css('h1 > span::text').extract_first()),
            'display': self.preprocess(response.css('div.display::text').extract_first()),
            'camera': self.preprocess(response.css('div.camera::text').extract_first()),
            'cpu': self.preprocess(response.css('div.cpu::text').extract_first()),
            'ram': self.preprocess(morespecs.css('span')[0].css('span > span::text').extract_first()),
            'memory': self.preprocess(morespecs.css('span')[2].css('span > span::text').extract_first()),
            'battery': self.preprocess(morespecs.css('span')[4].css('span > span::text').extract_first()),
        }

    def preprocess(self, text):
        if text == None : return None
        return unicodedata \
            .normalize('NFKD', text) \
            .encode('ascii', 'ignore') \
            .replace('\n', '').replace('\t', '').strip()
