import scrapy, logging, csv
from scrapy import Request

logger = logging.getLogger('logger_cnbc')

class CnbcSpider(scrapy.Spider):
    name = "cnbc"

    def start_requests(self):
        link = 'https://www.cnbcindonesia.com/tag/antm'
        yield scrapy.Request(url = link, callback=self.parse)


    def parse(self, response):
        list = []
        for url in response.selector.xpath('//ul[@class="list media_rows middle thumb terbaru gtm_indeks_feed"]/li/article/a').xpath('@href').getall():
            # logger.info('Elemen yang dipanggil %s', url)
            # print(url)
            yield Request(url, callback=self.parseContent, meta={}, dont_filter=True)
            #list.append(li)
        #print(list)

    def parseNextPage(self, response):
        pass

    def parseContent(self, response):
        dateTime    = response.css('.date::text').get()
        title       = response.xpath('//h1/text()').get()
        divContent  = response.xpath('//div[@class="detail_text"]')

        textContent = divContent.xpath('p/span/text()') if divContent.xpath('p/span').get() is not None else divContent.xpath('p/text()')
        #content     = [dateTime, title, newsContent]
        nextPage    = response.xpath('//div[contains(@class, "long-cta text-right")]')
        print(title, nextPage)
        if nextPage.get() is not None:
            link = nextPage.xpath('a').get()
            print(link)
        content     = []
        # divContent  = response.xpath('string(//div[class="detail_text"]/p/text())').extract()
        #print(divContent)
        for p in textContent.getall():
            content.append(p)
        finalContent = ' '.join(content)
        storeContent = [dateTime, title, finalContent]
        # print(storeContent)
