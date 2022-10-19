import scrapy

class Idx30Spider(scrapy.Spider):
    name = "idx30"

    def start_requests(self):
        # link = 'https://www.kontan.co.id/indeks-idx30'
        # link = 'https://www.infovesta.com/index/data_info/saham/idx30'
        # link = 'https://www.infojabodetabek.com/daftar-saham-indeks-idx30/'
        link = 'https://www.idxchannel.com/market-news/simak-daftar-saham-idx30-periode-agustus-2022-januari-2023-ada-3-saham-baru'
        yield scrapy.Request(url = link, callback=self.parse)

    def parse(self, response):
        # idx30_stock = {"code":[]}
        result      = []
        # content         = response.xpath('//table[@class="table table-bordered table-striped"]/tbody')
        # content         = response.xpath('//*[@class="wp-block-table"]/').getall()
        
        #content     = div.xpath('//table[class="table table-bordered table-striped"]/tbody')
        #content     = response.xpath('//div[@class="panel panel-default"]/table[@class="table table-bordered table-striped"]/tbody/tr/td[1]/text()').getall()
        content     = response.xpath('//div[@class="text-body--3"]/table/tbody/tr/td[3]/p/text()').extract()
        for index, data in enumerate(content):
            result.append(data)
        
        
        # print(idx30_stock)
        yield {"code" : result}

        