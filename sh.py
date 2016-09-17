#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import urllib.parse
import re
import sqlite3
from bs4 import BeautifulSoup


class Olx():
    DOMAIN = 'http://www.olx.ua/'
    CITIES = (
        'don', 'artemovsk', 'soledar', 'krasnyyliman',
        'kramatorsk', 'slavyansk', 'konstantinovka',
        'lisichansk', 'severodonetsk')
    db_name = 'dbarucars.db'

    def __init__(self, query, category='', subcategory='', city='',
                 min_price=0, max_price=0):
        self.make_url(query, category, subcategory, city,
                      min_price, max_price)

    def make_url(self, query, category, subcategory, city,
                 min_price, max_price):
        self.url = self.DOMAIN
        if category:
            self.url += category + '/'
            if subcategory:
                self.url += subcategory + '/'
        params_dict = {}
        if city:
            self.url += city + '/'
        if min_price:
            params_dict['search[filter_float_price%3Afrom]'] = min_price
        if max_price:
            params_dict['search[filter_float_price%3Ato]'] = max_price
        params = urllib.parse.urlencode(params_dict)
        self.url += 'q-' + urllib.parse.quote(query)
        self.url += '?' + params

    def get_page(self, page_id=0):
        #response = urlopen(self.url)
        #content = response.read()
        #content = content.decode('utf8')
        #with open('./olxpage.html', 'w', encoding='utf-8') as f:
        #    f.write(content)
        #s = BeautifulSoup(response.read())
        with open('./olxpage.html', 'r') as f:
            s = BeautifulSoup(f.read())
        ads = s.findAll('td', attrs={'class': 'offer'})
        #ads = s.find_all('table', attrs={'summary': 'Объявление'})
        # TODO what it's for
        re_price = re.compile('''<strong>(.*)</strong>''')

        for ad in ads:
            if len(str(ad)) < 100:
                continue
            # extracting image link
            tmp_tag = ad.find('img')
            if tmp_tag:
                img_src = tmp_tag['src']
            # extracting ad link
            # TODO promoted - remove it? mark it?
            tmp_tag = ad.find('a', attrs={'class': 'link'})
            ad_link = tmp_tag['href']
            title = tmp_tag.strong.contents[0]
            # extracting price
            tmp_tag = ad.find('p', attrs={'class': 'price'})
            price = re_price.search(str(tmp_tag.strong)).group(1)
            # TODO do i need location now?
            # extracting location
            #tmp_tag = ad.find(
            #    'p', attrs={'class': 'color-9 lheight16 marginbott5'})
            #location = tmp_tag.span.contents[0]
            #location = location.strip()
            # extracting date
            # TODO convert date
            tmp_tag = ad.find(
                'p',
                attrs={'class': 'color-9 lheight16 marginbott5 x-normal'})
            date = tmp_tag.contents[0]
            date = date.strip()
            ad_data = [title, date, price]
            #print(title, '||', price, '||', location, '||', date)
            #print('==========================')

    def save_to_db(self):
        tmp = [car_id,
               car['title'],
               car['addDate'],
               car['linkToView'],
               car['UAH'],
               car['USD'],
               car['modelName'],
               car['markName'],
               ]


def main():
    #cat = 'zhivotnye'
    #subcat = 'selskohozyaystvennye-zhivotnye'
    query = 'юмз'
    params = {
        'category': 'transport',
        'subcategory': '',
        'min_price': 15000,
        'max_price': 45000,
        #'currency': 'uah',
    }
    olx = Olx(query, **params)
    olx.get_page()
    return


if __name__ == "__main__":
    main()
