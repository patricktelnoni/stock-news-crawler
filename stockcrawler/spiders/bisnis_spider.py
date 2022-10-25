import scrapy, re

class BisnisSpider(scrapy.Spider):
    name = "bisnis"

    def start_requests(self):
        stock_list  = ['ADRO', 'ANTM', 'ARTO', 'ASII', 'BBCA', 'BBNI', 'BBRI', 'BMRI', 'BRPT', 'BUKA', 'CPIN', 'EMTK', 'GOTO', 'HRUM', 'ICBP', 'INCO', 'INDF', 'INKP', 'ITMG', 
                        'KLBF', 'MDKA', 'PGAS', 'PTBA', 'SMGR', 'TBIG', 'TINS', 'TLKM', 'TOWR', 'UNTR', 'UNVR']
        
        for stock in stock_list:
            link    = 'https://search.bisnis.com/?q={}'.format(stock.lower())
            yield scrapy.Request(url = link, callback=self.parse, meta={'kode_saham' : stock.lower()})

    def parse(self, response):
        kode_saham       = response.meta['kode_saham']
        pagination       = response.xpath('//ul[contains(class, "pages")]')
        max_page         = 1

        if pagination is not None:
            last_link       = response.xpath('//ul[@class="pages"]/li/a/@href').getall()[-1]
            query_string    = '(?<=per_page=)([^&]*)(?=&)?'
            max_page        = re.findall(query_string, last_link)
            print(max_page[0])
            
