# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import re



class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy

    def process_item(self, item, spider):
        # Здесь обработка item'a

            if spider.name == 'hhru':
                min_c = 'По договорённости'
                max_c = 'По договорённости'
                currency = ''
                vacancy_info_z = []
                for _ in item['salary']:
                    s = _.replace("\xa0", "")
                    vacancy_info_z.append(s)
                    # print(vacancy_info_z)
                item['salary'] = vacancy_info_z[0]
                #обработка зарплаты
                match1 = []
                if vacancy_info_z[0] != 'з/п не указана':
                    for a in re.split(r'-', vacancy_info_z[0]):
                        m = [el for el in re.findall(r'\d+', a)]
                        match1 = m
                    currency = vacancy_info_z[0].split()[-1]
                    # print(vacancy_info_z[0])
                    if re.fullmatch(r'от.* до.*', vacancy_info_z[0]):
                        min_c = int(match1[0])
                        max_c = int(match1[1])
                    elif ('от') in vacancy_info_z[0]:
                        min_c = int(match1[0])
                        max_c = 'По договорённости'
                    elif ('до') in vacancy_info_z[0]:
                        min_c = 'По договорённости'
                        max_c = int(match1[0])
                item['min'] = min_c
                item['max'] = max_c
                item['currency'] = currency
                item['website'] = 'hh.ru'

            elif spider.name == 'sjru':
                min_c = 'По договорённости'
                max_c = 'По договорённости'
                currency = ''
                vacancy_info_z = []
                o = ''
                match1 = []
                for _ in item['salary']:
                    s = _.replace("\xa0", "")
                    vacancy_info_z.append(s)
                    o = o + str(s)
                item['salary'] = o

                if vacancy_info_z[0] != 'По договорённости':
                    currency = o[-4:-1]
                    for a in re.split(r'—', o):
                        m = [el for el in re.findall(r'\d+', a)]
                        match1.append(m[0])
                if vacancy_info_z[0].startswith('от'):
                    min_c = int(match1[0])
                    max_c = 'По договорённости'
                elif vacancy_info_z[0].startswith('до'):
                    min_c = 'По договорённости'
                    max_c = int(match1[0])
                elif ('—') in vacancy_info_z:
                    min_c = int(match1[0])
                    max_c = int(match1[1])
                item['min'] = min_c
                item['max'] = max_c
                item['currency'] = currency
                item['website'] = 'superjob.ru'



            collection = self.mongobase[spider.name]
            collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)
            return item

class FotolmruPipeline:
    def process_item(self, item, spider):
        print()
        return item

class FotolmruPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                img = img.replace('w_82,h_82,', '')
                try:
                    yield scrapy.Request(img)
                except TypeError as e:
                    print(e)


    def item_completed(self, results, item, info):
        if results:
            item['link'] = item['link'][0]
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item