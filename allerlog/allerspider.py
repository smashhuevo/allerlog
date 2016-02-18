import scrapy
from scrapy.selector import Selector
import requests
import settings
import pprint

class AllerSpider(scrapy.Spider):
    name = 'allerspider'
    start_urls = ['http://www.houstontx.gov/health/Pollen-Mold/']

    def send_main_message(self, report_date, mail_body):
        return requests.post(
            settings.MAILGUN_URL,
            auth=("api", settings.MAILGUN_API_KEY),
            data={"from": settings.MAILGUN_FROM,
            "to": settings.MAILGUN_TO,
            "subject": "Allergy Report for " + report_date,
            "text": mail_body})

    def parse(self, response):

        report_date = response.selector.xpath('//table[@class="MsoNormalTable"]/tbody/tr/td/p/text()').extract_first()
        print report_date

        main_table = response.selector.xpath('//table[@class="MsoNormalTable"]/tbody/tr/td/div/table/tbody/tr/td/div/text()').extract()
        print main_table[3:6] # Tree
        print main_table[6:9] # Weed
        print main_table[9:12] # Grass
        print main_table[12:15] # Mold



        self.send_main_message(report_date, main_table[3:6])# yield scrapy.Request(response.urljoin(url), self.parse_titles)
