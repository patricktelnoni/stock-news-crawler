import scrapy

class Idx30Spider(scrapy.Spider):
    name = "idx30"

    def start_requests(self):
        link = 'https://www.kontan.co.id/indeks-idx30'
        yield scrapy.Request(url = link, callback=self.parse)

    def parse(self, response):
        idx30_stock = {"code":[]}
        result      = []
        content     = response.xpath('//table[@class="table table-bordered table-hover table-condensed"]/tbody')
        for index, data in enumerate(content.xpath('tr/td[2]/text()').getall()):
            if index < 30:
                result.append(data)
        
        idx30_stock["code"] = result
        yield idx30_stock 

        