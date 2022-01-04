# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import MovieItem


class TopmoviesSpider(scrapy.Spider):
    name = 'topMovies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/']

    def parse(self, response):
        links = response.css(".lister-list tr a::attr(href)").extract()
        for link in links:
            link = response.urljoin(link)
            print(link)
            yield scrapy.Request(url=link, callback=self.parse_details)

    def parse_details(self, response):
        json_res = json.loads(response.xpath(
            "//script[@type='application/ld+json']/text()").extract_first())
        film = MovieItem()
        if 'name' in json_res:
            film['name'] = json_res['name']
        if 'image' in json_res:
            film['image'] = json_res['image']
        if 'genre' in json_res:
            film['genre'] = json_res['genre']
        if 'contentRating' in json_res:
            film['contentRating'] = json_res['contentRating']
        if 'description' in json_res:
            film['description'] = json_res['description']
        if 'keywords' in json_res:
            film['keywords'] = json_res['keywords']    
        if 'duration' in json_res:
            film['duration'] = json_res['duration']

        yield film
