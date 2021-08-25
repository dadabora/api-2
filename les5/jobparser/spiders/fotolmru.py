import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import FotolmruItem
from scrapy.loader import ItemLoader


class FotolmruSpider(scrapy.Spider):
    name = 'fotolrmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super(FotolmruSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        goods_links = response.xpath("//a[contains(@class,'bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp')]")
        for link in goods_links:
            yield response.follow(link, callback=self.parse_good)

    def parse_good(self, response: HtmlResponse):
        loader = ItemLoader(item=FotolmruItem(), response=response)

        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('photos', "//img[contains(@slot,'thumbs')]/@src")
        loader.add_value('link', response.url)

        yield loader.load_item()



