
from urllib import request
import scrapy, json
from scrapy import Request

#logger = logging.getLogger('logger_cnbc')

class CnbcSpider(scrapy.Spider):
    name            = "cnbc"   
    def start_requests(self):
        file      = open('idx30.json')
        json_file = json.load(file)
        for emiten in json_file[0]["code"]:
            link = 'https://www.cnbcindonesia.com/tag/{}'.format(emiten.lower())
            #print(link)
            yield scrapy.Request(url = link, callback=self.parse, meta={'kode_saham' : emiten.lower()})
        file.close()
            
    def parse(self, response):
        kode_saham  = response.meta.get('kode_saham')
        
        paging      = response.xpath('//div[contains(@class, "paging")]')
        max_page    = 1
        
        if paging.get() is not None:
            max_page = max([page_number for page_number in paging.xpath('//a[@class=""]/text()').getall() if page_number.isnumeric()])
        
        for page_number in range(1, int(max_page)):
            #print(page_number, kode_saham)
            page_url = 'https://www.cnbcindonesia.com/tag/{}/{}'.format(kode_saham, page_number)
            # print(page_url)
            yield Request(page_url, callback=self.parsePage, meta={'kode_saham':kode_saham})
            
    def parsePage(self, response):
        kode_saham  = response.meta.get('kode_saham')
        for url in response.selector.xpath('//ul[@class="list media_rows middle thumb terbaru gtm_indeks_feed"]/li/article/a').xpath('@href').getall():
            yield Request(url, callback=self.parseContent, meta={'kode_saham':kode_saham})
    
    def parseNextPage(self, response):
        data        = response.meta.get('data')
        divContent  = response.xpath('//div[@class="detail_text"]')
        textContent = divContent.xpath('p/span/text()') if divContent.xpath('p/span').get() is not None else divContent.xpath('text()')
        for p in textContent.getall():
            data.append(p)
       # print(data)

    def parseContent(self, response):
        kode_saham  = response.meta.get('kode_saham')
        text_data   = []
        dateTime    = response.css('.date::text').get()
        title       = response.xpath('//h1/text()').get()
        div_content  = response.xpath('//div[@class="detail_text"]')
        #textContent = divContent.xpath('p/span/text()') if divContent.xpath('p/span').get() is not None else divContent.xpath('p/text()')
        if div_content.xpath('p').get() is not None:
            if len(div_content.xpath('p/span').getall()) > 0:
                text_content= div_content.xpath('p/span/text()')  
            else:
                text_content = div_content.xpath('p/text()')
        else:
            if div_content.xpath('span').get() is not None:
                text_content =  div_content.xpath('span/text()')
            else:
                text_content = div_content.xpath('text()')

        for p in text_content.getall():
            text_data.append(p)

        nextPage    = response.xpath('//div[contains(@class, "long-cta")]')
        if nextPage.get() is not None:
            link = nextPage.xpath('a/@href').get()
            # print(link, self.textResult)
            yield Request(link, callback=self.parseNextPage, meta={'data':text_data})

        finalContent = ' '.join(text_data)
        storeContent = [kode_saham, dateTime, title, finalContent]
        f = open('file.csv','a+')
        for data in storeContent:
            f.write("%s\n" % data)
        #print(storeContent)
