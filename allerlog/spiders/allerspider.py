import scrapy
import requests
import settings
import pprint
import jsonpickle
from scrapy.selector import Selector


class Allergen:

    def __init__(self, measurement_date, allergen_type, allergen_status, allergen_sum):
        self.measurement_date = measurement_date
        self.allergen_type = allergen_type
        self.allergen_status = allergen_status
        self.allergen_sum = allergen_sum


    measurement_date = None

    allergen_type = None
    allergen_status = None
    allergen_sum = None
    allergen_details = None

    def __repr__(self):
        from pprint import pformat
        return pformat(vars(self), indent=4, width=1)

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

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

        report_date = response.selector.xpath('//table[@class="MsoNormalTable"]/tbody/tr/td/p/strong/text()').extract_first()
        print report_date

        main_table = response.selector.xpath('//table[@class="MsoNormalTable"]/tbody/tr/td/div/table/tbody/tr/td/div/text()').extract()

        print "-----"

        print main_table

        print "-----"

        allergens = {'tree': Allergen(report_date, main_table[3], main_table[4], main_table[5]),
                     'weed': Allergen(report_date, main_table[6], main_table[7], main_table[8]),
                     'grass': Allergen(report_date, main_table[9], main_table[10], main_table[11]),
                     'mold': Allergen(report_date, main_table[12], main_table[13], main_table[14])
        }

        print allergens
        self.send_main_message(report_date, jsonpickle.encode(allergens))
