#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import sqlite3
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup


class Olx():
    DB_NAME = 'dbarucars.db'
    DOMAIN = 'http://www.olx.ua/'
    CITIES = (
        'don', 'artemovsk', 'soledar', 'krasnyyliman',
        'kramatorsk', 'slavyansk', 'konstantinovka',
        'lisichansk', 'severodonetsk')

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

    def get_page(self, page_id=1, from_web=True):
        if from_web:
            response = urlopen(self.url + '&page=' + str(page_id))
            content = response.read()
            content = content.decode('utf8')
            with open('./pageolx.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print('loading page:', self.url + '&page=' + str(page_id))
            s = BeautifulSoup(content)
        else:
            with open('./pageolx.html', 'r') as f:
                s = BeautifulSoup(f.read())

        ad_data = []
        ads = s.findAll('td', attrs={'class': 'offer'})

        # connecting to db
        conn = sqlite3.connect(self.DB_NAME)
        self.cursor = conn.cursor()

        for ad in ads:
            # empty ad
            if len(str(ad)) < 100:
                continue

            # extracting ad link and title
            tmp_tag = ad.find('a', attrs={'class': 'link'})
            url = tmp_tag['href']

            # position of the end of the link
            pos = url.find('html') + 4

            # TODO promoted link - remove it? mark it?
            # is the link promoted
            #if url.find('promoted') > 0:
            #    print('promoted')

            url = url[:pos]

            # check if ad in the db
            item_exists = self.cursor.execute(
                'select count(*) from olxcars where url=?',
                (url,)
                )

            if self.cursor.fetchone()[0]:
                continue

            print(url)
            #TODO remove any special symbols (.,'", etc.)
            title = tmp_tag.strong.contents[0].lower()

            # extracting image link
            tmp_tag = ad.find('img')
            if tmp_tag:
                img_src = tmp_tag['src']

            # extracting price
            tmp_tag = ad.find('p', attrs={'class': 'price'})
            tmp_price = tmp_tag.strong.contents[0]
            # remove 'грн.'
            tmp_price = tmp_price.split()
            price = ''.join(tmp_price[:-1])
            price = int(price)

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
            ad_date = tmp_tag.contents[0]
            ad_date = self.convert_date(ad_date)
            ad_data.append([title, url, ad_date, price])
        self.save_to_db(ad_data)
        conn.commit()
        conn.close()

    def convert_date(self, ad_date):
        ad_date = ad_date.strip()
        ad_date = ad_date.lower()
        if ad_date.find('сегодня') > -1:
            return datetime.date.today()
        if ad_date.find('вчера') > -1:
            return datetime.date.today() - datetime.timedelta(1)
        day, month_name = ad_date.split()

        months = {
            'янв.': '01', 'фев.': '02', 'март': '03', 'апр.': '04',
            'май': '05', 'июнь': '06', 'июль': '07', 'авг.': '08',
            'сент.': '09', 'окт.': '10', 'нояб.': '11', 'дек.': '12'}

        result = str(datetime.date.today().year) + '-' + months[month_name]
        result += '-' + day
        return result

    def save_to_db(self, ad_data):
        #create table olxcars (title char, url char, added datetime, uah int);
        self.cursor.executemany(
            'INSERT INTO olxcars VALUES (?,?,?,?)',
            ad_data)


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
    olx.convert_date('9 сент.')
    for i in range(1, 4):
        olx.get_page(page_id=i, from_web=True)
    return


if __name__ == "__main__":
    main()
