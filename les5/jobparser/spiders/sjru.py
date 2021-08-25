import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import SjruItem



class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=Data']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vacancies_links = response.xpath("//a[@target='_blank']/@href").extract()
        for link in vacancies_links:
            if '/vakansii/' in link:
                # print(link)
                yield response.follow(link, callback=self.vacancy_parse)




    def vacancy_parse(self, response: HtmlResponse):
        item_name = response.xpath("//h1/text()").extract_first()
        item_salary = response.xpath("//span[@class='_1h3Zg _2Wp8I _2rfUm _2hCDz']//text()").extract()
        item_link = response.url
        # print(item_link, item_name, item_salary)
        item = SjruItem(name=item_name, salary=item_salary, link=item_link)
        yield item