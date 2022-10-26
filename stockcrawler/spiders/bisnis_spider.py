from curses import meta
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
        
        for i in range(1, int(max_page[0])):
            link = 'https://search.bisnis.com/?q={}&per_page={}'.format(kode_saham, i)
            yield scrapy.Request(url=link, callback=self.iterate_page, meta={'kode_saham': kode_saham})
            

    def iterate_page(self, response):
        kode_saham  = response.meta['kode_saham']
        list_link   = response.xpath('//ul[@class="list-news"]/li/div[@class="col-sm-9"]/h2/a/@href').getall()

        for link in list_link:
            yield scrapy.Request(url=link, call_back=self.parse_content, meta={'kode_saham': kode_saham})

    def parse_content(self, response):
        kode_saham       = response.meta['kode_saham']

        title   = response.xpath('//h1[@class="title-only]/text()').extract_first()
        content = response.xpath('//div[@class="col-sm-10 col-sm-offset-2"]/p/text()').getall()
        date    = response.xpath('//div[@class="news-description"]/span//text()').get()
        
        yield{
            'saham'             : kode_saham,
            'tanggal_berita'    : date,
            'judul'             : title,
            'isi'               : ' '.join(content)
        }

            
