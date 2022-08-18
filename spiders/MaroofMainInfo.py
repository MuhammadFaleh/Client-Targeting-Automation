import time
from datetime import datetime
import json
from urllib.parse import urlparse
import numpy as np
import requests
import scrapy
import twint
from dateutil.relativedelta import relativedelta
from scrapy.loader import ItemLoader
from items import MarofItem


class MarofMainInfoSpider(scrapy.Spider):
    name = 'main_info'
    allowed_domains = ['maroof.sa']

    def __init__(self):
        # used for the post request in comment_count
        self.websiteCheck = ["snap", "tiktok", "maroof", "/t.me/", "Maroof", 'twitter', 'instagram', 'wa.me/']
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US;q=0.9,en;q=0.8,en-GB;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': 'RefreshFilter=; Maroof_CK=!lEg2VTugEQeSQ1U1KzEZZdBR1kPqM3sPIU4DNxLpirDM2dTJCKSUPqqgFCKjY3h/jcB6AfzjZ1xzdg==; _ga=GA1.2.1563102204.1655984632; _jsuid=3599925798; __RequestVerificationToken=SJJlXelg0FIlxsQWSmXDltLEJDPWINOZlF3cYr27-UcybBUxsAG0Re1MrzAAJM3yqOPU3z8Vel9Uwd79uisoY3YeqYLXmwUGbCWLkFwhcxo1; _gid=GA1.2.697557126.1656571145; _no_tracky_100935705=1; TS01281e28=01ae665f6e72b8fc13683ad08a2d43c014b47ed64d81cc39e12f2551268509e4bb5c4a628542e377df471585b931989e71b0ebaa4907916df6d291ff822065cabc920b321d89dd0ad427d9f9ab3df3125718e5c821e06aa13598045069a33580c2eb3c88c7; _gat_UA-92820988-1=1; TSafcb07d9027=085e8b4c78ab2000087aab08440f11707a134d1dfb377dc19c78e46cbb116f6ff29680bcaf73fb33081233d811113000352cfe4de76fbb8f103465bc1c36bd3e7b051a245adabf21dff3c9be2fb07784fc3de1937d0fb1e072eeba922c52952e; RefreshFilter=; TS01281e28=01ae665f6e519b658608e99c0acf7697af5b99f1c2ee50a08ddf8f776f6b364ded4a9bf325e926d1f0a9ade6dd7414387abad51b9c8972bb369202d8d0515ccc4b17f027848c2ec516452ce3539cacd3a8a383b8c33c3b9e86c1fe4f12df0dd95813a939c1; TSafcb07d9027=085e8b4c78ab2000a3bd70c0c0c07e3df2d8ff3f5c0b1fd743e9c51f29329a051913a827ad4795c50883b9011411300029ce218b3f2cf5204172d84410bd3639b2a48deae2d94168ffa8b148f9fae05f331e5ffeefcc7d8bf38508a5f0162fa8',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'traceparent': '00-3c884f19887c9d0b1cc0eca8c9633eac-f14c23a8f95950bb-01'

        }

    def start_requests(self):
        list_pages = [47, 45, 25, 39, 48, 26, 51, 23, 24, 41, 35, 49, 34, 14, 16]
        for i in list_pages:
            next_page = f'https://maroof.sa/BusinessType/MoreBusinessList?businessTypeId={i}&pageNumber={0}' \
                        f'&sortProperty=BestRating&desc=True'
            page_url = f'https://maroof.sa/BusinessType/MoreBusinessList?businessTypeId={i}' + '&pageNumber='
            time.sleep(0.010)
            yield scrapy.Request(next_page, callback=self.request_pages, meta={'page_Url': page_url})

    def request_pages(self, response):
        get_ = requests.get(str(response.meta['page_Url']) + str(0) +
                            f'&sortProperty=BestRating&desc=True')
        src = get_.json()
        count_ = int(src["Count"]) // 10
        if count_ >= 999:  # server doesn't show any elements after 10k
            count_ = 999
        for i in range(0, count_ + 1):
            next_page = str(response.meta['page_Url']) + str(i) + '&sortProperty=BestRating&desc=True'
            time.sleep(0.010)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        for i in data['Businesses']:  # slow
            if i['Url'] is not None:
                link = "https://maroof.sa" + str(i['Url'])
                ID = int(str(i['Url']).replace("/", ""))
                name = str(i['NameAr']).strip()
                rating = float(i['Rating'])
                raters = float(i['RatingNum'])
                Crnum = i['CRNumber']
                Tname = i['TypeName']
                yield scrapy.Request(
                    link, callback=self.parse_links,
                    meta={'ID': ID, 'Name': name, 'Rating': rating, 'Ratters': raters, 'CRNumber': Crnum, 'link': link,
                          'type': Tname})
            else:
                break

    def comment_count(self, link, count, curr, prev, visit_counter):  # slow (jump pages by ordering algo)
        get_ = requests.post(link + '/' + str(curr), headers=self.headers)
        src = get_.json()
        comment_num = 0
        for i in src['Comment']:
            date = str(i['CreationDate'])
            try:
                date2 = datetime.strptime(date[6:-7].strip(), '%d-%m-%Y')
            except:
                date2 = datetime.strptime(date[7:-7].replace("ء", "").strip(), '%d-%m-%Y')
            if date2 > datetime.today() - relativedelta(month=3):
                comment_num += 1
                count = (curr * 4) + comment_num

        if 0 < comment_num < 4:
            return count

        if visit_counter == curr - 1 and comment_num == 0:
            return count

        if comment_num == 4:
            visit_counter = curr
            curr += prev
            return self.comment_count(link, count, curr, prev, visit_counter)

        if comment_num == 0 and 0 < curr:
            curr -= prev
            prev = 1
            return self.comment_count(link, count, curr, prev, visit_counter)

        return count

    def parse_links(self, response):
        if response.meta['Ratters'] != 0:
            count_comment = self.comment_count(response.meta['link'], 0, 0, 10, 0)
        else:
            count_comment = 0
        web = str(response.xpath("//div/div/p[contains(text(), 'الموقع الإلكتروني')]/following-sibling::p/a/@href").get())
        twit = str(response.xpath("//div/div/p[contains(text(), 'تويتر')]/following-sibling::p/a/@href").get())
        insta = str(response.xpath("//div/div/p[contains(text(), 'إنستجرام')]/following-sibling::p/a/@href").get())

        if 'twitter' in web and web is not None:
            twit = web + ""
            web = None
        elif 'instagram' in web and web is not None:
            insta = web
            web = None
        elif any(key in web for key in self.websiteCheck):
            web = None

        item = ItemLoader(item = MarofItem(), selector=response)
        item.add_value('Name', response.meta['Name'])
        item.add_value('Activity', response.meta['type'])
        item.add_value('CRNumber', response.meta['CRNumber'])
        item.add_value('Rating', response.meta['Rating'])
        item.add_value('Ratters', response.meta['Ratters'])
        item.add_value('ResComments',  count_comment)
        item.add_xpath('Phone', "//div/div/p[contains(text(), 'رقم الجوال')]/following-sibling::p/a/@href")
        item.add_xpath('Email', "//div/div/p[contains(text(), 'البريد')]/following-sibling::p/a/@href")

        # likes , rep , ret
        item.add_value('Twitter',  twit)
        item.add_value('Insta', insta)

        item.add_xpath('Whatsapp', "//div/div/p[contains(text(), 'واتس')]/following-sibling::p/a/@href")
        item.add_xpath('Location', "//div/div/p[contains(text(), 'عنوان المتجر')]/following-sibling::p/text()[3]")

        item.add_value('Website', web)
        item.add_xpath('Android',  "//div/div/p/a[contains(@href, 'https://play')]/@href")

        item.add_xpath('IOS', "//div/div/p/a[contains(@href, 'https://apps/')]/@href")

        yield item.load_item()
