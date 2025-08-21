import scrapy, re

class InvestoridSpider(scrapy.Spider):
    name ="investorid"

    def start_requests(self):
        stock_list  = ['ADRO', 'ANTM', 'ARTO', 'ASII', 'BBCA', 'BBNI', 'BBRI', 'BMRI', 'BRPT', 'BUKA', 'CPIN', 'EMTK', 'GOTO', 'HRUM', 'ICBP', 'INCO', 'INDF', 'INKP', 'ITMG',
                        'KLBF', 'MDKA', 'PGAS', 'PTBA', 'SMGR', 'TBIG', 'TINS', 'TLKM', 'TOWR', 'UNTR', 'UNVR']
        
        for stock in stock_list:
            link    = 'https://investor.id/search/{}'.format(stock.lower())
            yield scrapy.Request(url=link, callback=self.parse, meta={'kode_saham': stock.lower()})

    def parse(self, response):
        kode_saham       = response.meta['kode_saham']
        pagination       = response.xpath('//ul[contains(@class, "pagination")]')
        max_page         = 1
        '''
        if pagination is not None:
            last_link       = response.xpath('//ul[@class="pagination"]/li/a/@href').getall()[-1]
            query_string    = '(?<=page-item=)([^&]*)(?=&)?'
            max_page        = re.findall(query_string, last_link)
            '''
        
        for i in range(1, 15):
            link = f'https://investor.id/search/{kode_saham}/{i}'
            yield scrapy.Request(url=link, callback=self.iterate_page, meta={'kode_saham': kode_saham})

    def iterate_page(self, response):
        kode_saham  = response.meta['kode_saham']
        list_link   = response.xpath("(//div[@class='id-grid mx-auto mt-4'])[2]//a[@class='stretched-link']/@href").extract()
    
        print(list_link)
        for link in list_link:
            link = 'https://investor.id' + link
            yield scrapy.Request(url=link, callback=self.parse_content, meta={'kode_saham': kode_saham})

    def parse_content(self, response):
        kode_saham       = response.meta['kode_saham']

        title   = response.xpath('//h1[@class="h2"]/text()').extract_first()
        content = response.xpath('//div[@class="col fsbody2 body-content"]/p/text()').extract()

        yield{
            'saham'             : kode_saham,
            'judul'             : title,
            'isi'               : ''.join(content)
        }
