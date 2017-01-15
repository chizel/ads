#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import datetime
import urllib.parse
import urllib.error
import urllib.request
from bs4 import BeautifulSoup


class Olx():
    DOMAIN = 'https://www.olx.ua/'
    CITIES = (
        'don', 'artemovsk', 'soledar', 'krasnyyliman',
        'kramatorsk', 'slavyansk', 'konstantinovka',
        'lisichansk', 'severodonetsk')

    MONTHS = {'янв.': '01', 'фев.': '02', 'март': '03', 'апр.': '04',
              'май': '05', 'июнь': '06', 'июль': '07', 'авг.': '08',
              'сент.': '09', 'окт.': '10', 'нояб.': '11', 'дек.': '12'}

    def __init__(self, query, db_name, table_name, category='', subcategory='',
                 city='', min_price=0, max_price=0):
        self.db_name = db_name
        self.table_name = table_name
        self.make_url(query, category, subcategory, city,
                      min_price, max_price)

    def make_url(self, query, category, subcategory, city,
                 min_price, max_price):
        '''Generating url'''
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
        self.url += '/?' + params

    def get_page(self, page_id=1, from_web=True):
        '''retrieving web page'''
        if from_web:
            page_url = self.url
            if page_id > 1:
                page_url += '&page=' + str(page_id)

            req = urllib.request.Request(page_url)
            req.add_header(
                'user-agent',
                '''Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36
                (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'''
                )
            try:
                response = urllib.request.urlopen(req)
            except urllib.error.HTTPError as e:
                print('Error! %s' % e)
                print('Page isn\'t loaded! Url: ', page_url)
                return

            if response.url != page_url:
                print('REDIRECT!', page_url)
                return 'Redirect'

            content = response.read()
            content = content.decode('utf8')

            if content.find('Не найдено ни одного объявления') > -1:
                print('Не найдено ни одного объявления: ', page_url)
                return

            # saving page to the fie
            with open('./tmp/pageolx.html', 'w', encoding='utf-8') as f:
                f.write(content)

            print('loading page:', page_url)
            s = BeautifulSoup(content)
        else:
            # for testing load from local file
            with open('./tmp/pageolx.html', 'r') as f:
                s = BeautifulSoup(f.read())

        ad_data = []
        ads = s.findAll('td', attrs={'class': 'offer'})

        # connecting to db
        conn = sqlite3.connect(self.db_name)
        self.cursor = conn.cursor()

        # query for checking is item already in the db
        check_query = 'select count(*) from '
        check_query += self.table_name
        check_query += ' where url=?'

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
            item_exists = self.cursor.execute(check_query, (url,))
            if self.cursor.fetchone()[0]:
                continue

            print(url)
            #TODO remove any special symbols (.,'", etc.)
            title = tmp_tag.strong.contents[0].lower()

            # extracting image link
            tmp_tag = ad.find('img')
            if tmp_tag:
                image = tmp_tag['src']
            else:
                image = ''

            # extracting price
            tmp_tag = ad.find('p', attrs={'class': 'price'})
            tmp_price = tmp_tag.strong.contents[0]

            if tmp_price.lower() == 'обмен':
                price = -1
            else:
                # remove 'грн.'
                tmp_price = tmp_price.split()
                price = ''.join(tmp_price[:-1])
                price = int(price)

            # extracting location
            tmp_tag = ad.find(
                'p', attrs={'class': 'color-9 lheight16 marginbott5'})
            location = tmp_tag.span.contents[0]
            location = location.strip()

            # extracting date
            tmp_tag = ad.find(
                'p',
                attrs={'class': 'color-9 lheight16 marginbott5 x-normal'})
            ad_date = tmp_tag.contents[0]
            ad_date = self.convert_date(ad_date)
            ad_data.append([url, title, price, ad_date, location, image])
        self.save_to_db(ad_data)
        conn.commit()
        conn.close()

    def convert_date(self, ad_date):
        '''Converting date to standart'''
        ad_date = ad_date.strip()
        ad_date = ad_date.lower()
        if ad_date.find('сегодня') > -1:
            return datetime.date.today()
        if ad_date.find('вчера') > -1:
            return datetime.date.today() - datetime.timedelta(1)
        day, month_name = ad_date.split()

        # add 0
        if len(day) == 1:
            day = '0' + day

        # current year or previous
        if datetime.date.today().month < int(self.MONTHS[month_name]):
            result = str(datetime.date.today().year - 1)
        else:
            result = str(datetime.date.today().year)

        result += '-' + self.MONTHS[month_name]
        result += '-' + day
        return result

    def save_to_db(self, ad_data):
        query_string = 'INSERT OR IGNORE INTO '
        query_string += self.table_name
        query_string += '(url, title, uah, added, location, image)'
        query_string += 'VALUES (?,?,?,?,?,?)'
        self.cursor.executemany(query_string, ad_data)


def main():
    query = 'юмз'
    params = {
        'db_name': 'ads.db',
        'table_name': 'tractors',
        'category': 'transport',
        'subcategory': '',
        'min_price': 20000,
        'max_price': 40000,
        #'currency': 'uah',
    }
    olx = Olx(query, **params)

    for i in range(1, 10):
        resp = olx.get_page(page_id=i, from_web=True)
        if resp == 'Redirect':
            return


if __name__ == "__main__":
    main()
