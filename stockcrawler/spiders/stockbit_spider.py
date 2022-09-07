from urllib import request
import scrapy, json
from scrapy.http.request.json_request import JsonRequest


class StockbitSpider(scrapy.Spider):
    name = "stockbit"
    # start_urls = ['https://stockbit.com/login']
    
    def get_month(self, month_name):
        swithcer={
            "Jan":1,
            "Feb":2,
            "Mar":3,
            "Apr":4,
            "May":5,
            "Jun":6,
            "Jul":7,
            "Aug":8,
            "Sep":9,
            "Oct":10,
            "Nov":11
        }
        return swithcer.get(month_name, 12)

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

        file      = open('idx30.json')
        json_file = json.load(file)
        for emiten in json_file[0]["code"]:
            url = 'https://exodus.stockbit.com/seasonality/{}?year=2022&back_year=10'.format(emiten.lower())
            #print(link)
            yield scrapy.Request(url = url, headers=header, method='GET', meta={'kode_saham' : emiten.lower()}, callback=self.parse_seasonality)
        file.close()
        url          = 'https://exodus.stockbit.com/seasonality/ANTM?year=2022&back_year=10'    
        
        
    def parse_seasonality(self, response):
        kode_saham      = response.meta['kode_saham']
        data            = json.loads(response.text)
        price_change    = data['data']['price_change']
        for price_year in price_change:
            year    = price_year['row']
            for index, monthly_data in enumerate(price_year['columns']):
                if monthly_data['name'] != 'Year':
                    month_num = self.get_month(monthly_data['name'])
                    yield {
                        'stock'     : kode_saham,
                        'change'    : monthly_data['value'],
                        'month'     : month_num,
                        'year'      : year,
                        'status'    : 'negative' if float(monthly_data['value']) < 0  else 'positive'
                    }


