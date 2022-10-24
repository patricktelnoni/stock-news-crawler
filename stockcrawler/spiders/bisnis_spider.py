import scrapy
import re

class BisnisSpider(scrapy.Spider):
    name = "bisnis.com"

    def start_request(self):
        stock_list  = ['ADRO', 'ANTM', 'ARTO', 'ASII', 'BBCA', 'BBNI', 'BBRI', 'BMRI', 'BRPT', 'BUKA', 'CPIN', 'EMTK', 'GOTO', 'HRUM', 'ICBP', 'INCO', 'INDF', 'INKP', 'ITMG', 'KLBF', 'MDKA', 'PGAS', 'PTBA', 'SMGR', 'TBIG', 'TINS', 'TLKM', 'TOWR', 'UNTR', 'UNVR']
        
        for emiten in stock_list:
            link = 'https://bisnis.com/?q={}'.format(emiten.lower())
            print(link)
            yield scrapy.Request(url = link, callback=self.parse, meta={'kode_saham' : emiten.lower()})

    def parse(self, response):
        kode_saham       = response.meta['kode_saham']
        pagination       = response.xpath('//ul[contains(class, "pages")]')
        max_page         = 1
        print(kode_saham)
        if pagination is not None:
            last_link       = response.xpath('//ul[@class="pages"]/li/a/@href').getall()[-1]
            query_string    = '(?<=per_page=)([^&]*)(?=&)?'
            max_page        = re.findall(query_string, last_link)
            
