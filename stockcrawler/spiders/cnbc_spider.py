import scrapy, logging, csv
from scrapy import Request

logger = logging.getLogger('logger_cnbc')

class CnbcSpider(scrapy.Spider):
    name            = "cnbc"   
    # textResult      = []
    def start_requests(self):
        link = 'https://www.cnbcindonesia.com/tag/antm'
        yield scrapy.Request(url = link, callback=self.parse)


    def parse(self, response):
        for url in response.selector.xpath('//ul[@class="list media_rows middle thumb terbaru gtm_indeks_feed"]/li/article/a').xpath('@href').getall():
            yield Request(url, callback=self.parseContent)


    def parseNextPage(self, response):
        data        = response.meta.get('data')
        divContent  = response.xpath('//div[@class="detail_text"]')
        textContent = divContent.xpath('p/span/text()') if divContent.xpath('p/span').get() is not None else divContent.xpath('p/text()')
        for p in textContent.getall():
            data.append(p)
        print(data)

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
        print(storeContent)
