from calendar import month
from urllib import request
import scrapy, json

#from playwrigth.async_api import async_playwright

class KontanSpider(scrapy.Spider):
    name        = "kontan"
    #list_link   = []

    def start_requests(self):
        # file      = open('idx30.json')
        # json_file = json.load(file)
        stock_list  = ['ADRO', 'ANTM', 'ARTO', 'ASII', 'BBCA', 'BBNI', 'BBRI', 'BMRI', 'BRPT', 'BUKA', 'CPIN', 'EMTK', 'GOTO', 'HRUM', 'ICBP', 'INCO', 'INDF', 'INKP', 'ITMG', 'KLBF', 'MDKA', 'PGAS', 'PTBA', 'SMGR', 'TBIG', 'TINS', 'TLKM', 'TOWR', 'UNTR', 'UNVR']
        for emiten in stock_list:
            link = 'https://www.kontan.co.id/tag/saham-{}'.format(emiten.lower())
            #print(link)
            yield scrapy.Request(url = link, callback=self.parse, meta={'kode_saham' : emiten.lower()})
        # file.close()


    def parse(self, response):
        kode_saham       = response.meta['kode_saham']
        pagination       = response.xpath('//div[contains(class, "stream-loadmore")]')

        #list_link       = response.xpath('//ul[@id="load_berita"]/li/a/@href').getall()
        #print(list_link)
        if pagination is not None:
            for i in range(4):
                next_page = 'https://www.kontan.co.id/tag/loadmore_news/saham-{}/{}'.format(kode_saham, i*10)
                # self.parse_next(list_link, next_page)
                yield scrapy.Request(url=next_page, callback=self.parse_nextlink, meta={'kode_saham':kode_saham})

    def parse_nextlink(self, response):
        #list_link       = response.meta['list_link']
        kode_saham       = response.meta['kode_saham']
        nextpage_link   = response.xpath('//li/a/@href').getall()
        
        for link in nextpage_link:
            yield scrapy.Request(url='https:'+link, callback=self.parse_content, meta={'kode_saham':kode_saham})

    def parse_content(self, response):
        kode_saham      = response.meta['kode_saham']  

        judul           = response.xpath('//h1[@class="jdl_dtl"]/text()').extract() if response.xpath('//h1[@class="jdl_dtl"]').get() is not None else response.xpath('//h1[@class="detail-desk"]/text()').extract_first()
        content         = response.xpath('//div[@class="tmpt-desk-kon"]/p/text()').extract() if response.xpath('//div[@class="tmpt-desk-kon"]').get() is not None else response.xpath('//div[@class="ctn"]/p/text()').extract()
        tanggal_berita  = ""

        if response.xpath('//div[@class="fs13 color-gray mar-t-10"]').get() is not None:
            tanggal_berita = response.xpath('//div[@class="fs13 color-gray mar-t-10"]/text()').extract()[0]
        elif response.xpath('//div[@class=" fs14 ff-opensans font-gray"]/text()').get() is not None: 
            tanggal_berita = response.xpath('//div[@class=" fs14 ff-opensans font-gray"]/text()').extract()[1]
        else:
            datestamp = response.xpath('//div[@class=''date]')
            month = datestamp.xpath('/div[@class="mm"]')
            day = datestamp.xpath('/div[@class="dd"]')
            year = datestamp.xpath('/div[@class="yy"]')
            tanggal_berita = '{} {} {}'.format(day, month, year)

        full_text   = ' '.join(content[5:])
    
        yield{
            'saham':kode_saham,
            'tanggal_berita':tanggal_berita,
            'judul' : judul,
            'isi':full_text
        }
        
    