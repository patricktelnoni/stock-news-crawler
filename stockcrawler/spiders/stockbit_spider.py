import scrapy, json
from scrapy.http.request.json_request import JsonRequest


class StockbitSpider(scrapy.Spider):
    name = "stockbit"
    # start_urls = ['https://stockbit.com/login']
    
    def start_requests(self):
        # login = 'https://stockbit.com/login'
        login = 'https://stockbit.com/api/login/email'
        link = 'https://stockbit.com/#/symbol/ANTM/keystats'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'isLoggedIn=true'
            }
   
        yield scrapy.Request(url = login, method='POST', headers=headers, body='username=&password=', callback=self.parse)
    
    def parse(self, response):
       data         = json.loads(response.text)
       access_token = data['data']['access_token']
       header       = {'Authorization': 'Bearer {}'.format(access_token)}
       url          = 'https://exodus.stockbit.com/seasonality/ANTM?year=2022&back_year=10'    
       yield scrapy.Request(url = url, headers=header, method='GET', callback=self.parse_seasonality)
        
    def parse_seasonality(self, response):
        pass

    
        