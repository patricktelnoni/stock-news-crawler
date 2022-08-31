
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
            print(link)
            yield scrapy.Request(url = link, callback=self.parse)
        file.close()
            
    def parse(self, response):
        paging      = response.xpath('//div[contains(@class, "paging")]')
        max_page    = 1
        if paging.get() is not None:
            max_page = max([page_number for page_number in paging.xpath('//a[@class=""]/text()').getall() if page_number.isnumeric()])
            
        for page_number in range(1, int(max_page)):
            page_url = 'https://www.cnbcindonesia.com/tag/antm/{}'.format(page_number)
            yield Request(page_url, callback=self.parsePage)
            
    def parsePage(self, response):
        for url in response.selector.xpath('//ul[@class="list media_rows middle thumb terbaru gtm_indeks_feed"]/li/article/a').xpath('@href').getall():
            yield Request(url, callback=self.parseContent)
    
    def parseNextPage(self, response):
        data        = response.meta.get('data')
        divContent  = response.xpath('//div[@class="detail_text"]')
        textContent = divContent.xpath('p/span/text()') if divContent.xpath('p/span').get() is not None else divContent.xpath('p/text()')
        for p in textContent.getall():
            data.append(p)
       # print(data)

    def parseContent(self, response):
        textData    = []
        dateTime    = response.css('.date::text').get()
        title       = response.xpath('//h1/text()').get()
        divContent  = response.xpath('//div[@class="detail_text"]')
        textContent = divContent.xpath('p/span/text()') if divContent.xpath('p/span').get() is not None else divContent.xpath('p/text()')

        for p in textContent.getall():
            textData.append(p)

        nextPage    = response.xpath('//div[contains(@class, "long-cta")]')
        if nextPage.get() is not None:
            link = nextPage.xpath('a/@href').get()
            # print(link, self.textResult)
            yield Request(link, callback=self.parseNextPage, meta={'data':textData})

        finalContent = ' '.join(textData)
        storeContent = [dateTime, title, finalContent]
        f = open('file.csv','a+')
        for data in storeContent:
            f.write("%s\n" % data)
        #print(storeContent)
