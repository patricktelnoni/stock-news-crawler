import scrapy

class StockbitSpider(scrapy.Spider):
    name = "stockbit"

    def start_requests(self):
        link = 'https://stockbit.com/#/symbol/ANTM/keystats'
        yield scrapy.Request(url = link, callback=self.parse)

    def parse(self, response):
        print(response)

        