# to run 
# scrapy crawl tmdb_spider -o movies.csv -a subdir=27205-inception

import numpy as np
import pandas as pd
import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    def __init__(self, subdir=None, *args, **kwargs):
        super(TmdbSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://www.themoviedb.org/movie/{subdir}/"]

    def parse(self, response):
        full_credits_url = f"{self.start_urls[0]}cast"
        yield scrapy.Request(full_credits_url, callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        credits = response.css('ol.people.credits')[0]
        actor_links = credits.css('div.info a::attr(href)').getall()
        for actor in actor_links:
            actor_url = response.urljoin(actor)
            yield scrapy.Request(actor_url, self.parse_actor_page)

    def parse_actor_page(self, response):
        actor_name = response.css('div.title a::text').get()
        acting_index = 0
        jobs = response.css('div.credits_list h3::text').getall()
        for i in range(len(jobs)):
            if jobs[i] == 'Acting':
                acting_index = i
                break
        acting_cred = response.css('div.credits_list table.card.credits')[acting_index]
        movie_or_TV_names = acting_cred.css('bdi::text').getall()
        for movie_or_TV_name in movie_or_TV_names:
            yield {
                "actor" : actor_name,
                "movie_or_TV_name" : movie_or_TV_name
            }