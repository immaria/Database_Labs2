# -*- coding: utf-8 -*-
from scrapy.http.response import Response
import scrapy


class RozetkaSpider(scrapy.Spider):
    name = 'rozetka'
    allowed_domains = ['www.rozetka.com.ua']
    start_urls = ['https://rozetka.com.ua/make_up_acessories/c2048527/']

    def parse(self, response: Response):
        products = response.xpath("//div[contains(@class, 'goods-tile__inner')]")[:20]
        for product in products:
            yield {
                    'description': product.xpath(".//a[@class='goods-tile__heading']/@title").get(),
                    'price': product.xpath(".//span[@class='goods-tile__price-value']/text()").get(),
                     'img': product.xpath(".//img[@class='lazy_img_hover display-none']/@data-url").get()
            }