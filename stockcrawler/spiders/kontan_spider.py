import scrapy, json
#from playwrigth.async_api import async_playwright

class KontanSpider(scrapy.Spider):
    name = "kontan"

    def start_requests(self):
        file      = open('idx30.json')
        json_file = json.load(file)
        for emiten in json_file[0]["code"]:
            link = 'https://www.kontan.co.id/tag/saham-{}'.format(emiten.lower())
            #print(link)
            yield scrapy.Request(url = link, callback=self.parse, meta={'kode_saham' : emiten.lower()})
        file.close()


    def parse(self, response):
        kode_saham       = response.meta.get('kode_saham')
        pagination       = response.xpath('//div[contains(class, "stream-loadmore")]')

        list_link_berita = response.xpath('//ul[@id="load_berita"]/li/a/@href').getall()
        if pagination is not None:
            print('ada pagination')
        print(kode_saham, pagination)
        # next page = https://www.kontan.co.id/tag/loadmore_news/saham-tbig/10

        ''' url = response.meta.get('url')
        div_content  = response.xpath('//div[@class="detail_text"]')
        if div_content.xpath('p').get() is not None:
            if len(div_content.xpath('p/span').getall()) > 0:
                print('p contain span', div_content.xpath('p/span/text()').extract())
                
            else:
                print('p without span', div_content.xpath('p/text()').extraxct())
        else:
            if div_content.xpath('span').get() is not None:
                print('no p but with span', div_content.xpath('span/text()').extract())
            else:
                print('no span and no p', div_content.xpath('text()').extract())
        #text_content = div_content.xpath('p/span/text()') if div_content.xpath('p/span').get() is not None else div_content.xpath('/text()')
        # print(div_content.xpath('span/text()').extract())
        # print(div_content.xpath('text()').extract())
       # print(div_content.xpath('text()').extract())
       '''