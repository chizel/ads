#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import datetime
import urllib.error
import urllib.request
from bs4 import BeautifulSoup


class Rstua():
    DOMAIN = 'http://rst.ua/'

    def __init__(self, category, db_name, table_name,
                 min_price=0, max_price=0):
        self.db_name = db_name
        self.table_name = table_name
        self.make_url(category, min_price, max_price)

    def make_url(self, category, min_price, max_price):
        self.url = self.DOMAIN + 'oldcars/'
        self.url += category + '/?'

        if min_price:
            self.url += 'price[]=' + str(min_price) + '&'
        if max_price:
            self.url += 'price[]=' + str(max_price) + '&'

    def get_page(self, page_id=1, from_web=True):
        if from_web:
            page_url = self.url + 'start=' + str(page_id)

            try:
                response = urllib.request.urlopen(page_url)
            except urllib.error.HTTPError as e:
                print('Error! %s' % e)
                print('Page isn\'t loaded! Url: ', page_url)
                return

            content = response.read()
            content = content.decode('windows-1251')

            with open('./tmp/pagerst.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print('Loading page:', page_id)
            s = BeautifulSoup(content)
        else:
            with open('./tmp/pagerst.html', 'r') as f:
                s = BeautifulSoup(f.read())

        # connecting to db
        conn = sqlite3.connect(self.db_name)
        self.cursor = conn.cursor()

        ad_data = []
        ads = s.findAll('div', attrs={'class': 'rst-ocb-i '})
        loaded = False

        for ad in ads:
            tmp_tag = ad.find('a')
            url = self.DOMAIN[:-1]
            url += tmp_tag['href']

            # check if ad in the db
            query_str = 'SELECT COUNT(*) FROM '
            query_str += self.table_name
            query_str += ' WHERE url=?'
            item_exists = self.cursor.execute(query_str, (url,))
            if self.cursor.fetchone()[0]:
                # ad already in db, nothing to do
                continue

            title = tmp_tag.span.contents[0]
            title = title.lower()

            # I need only UMZ without MTZ
            if title.find('юмз') == -1 or title.find('мтз') > -1:
                continue

            print('Loading : ', url)
            loaded = True
            image = tmp_tag.img['src']

            uah = ad.ul.contents[0].span.contents[0]
            # remove грн
            uah = uah.split()[0]
            # remove '
            uah = ''.join(uah.split("'"))
            try:
                uah = int(uah)
            except:
                uah = 0

            location = ad.ul.contents[1].span.contents[0]
            tmp_tag = ad.find('div', attrs={'class': 'rst-ocb-i-s'})
            ad_date = self.make_date(tmp_tag.contents[1])
            ad_data.append([url, title, uah, ad_date, location, image])

        if loaded:
            self.save_to_db(ad_data)
            conn.commit()
            conn.close()
        return loaded

    def make_date(self, sdate):
        date_info = sdate.split()
        if len(date_info) < 2:
            return datetime.date.today()
        d, m, y = date_info[1].split('.')
        return y + '-' + m + '-' + d

    def save_to_db(self, ad_data):
        #create table rstcars (title char, url char primary key unique,
               # uah int, added datetime, location char, image_link char);
        query_string = 'INSERT OR IGNORE INTO '
        query_string += self.table_name
        query_string += '(url, title, uah, added, location, image)'
        query_string += 'VALUES (?,?,?,?,?,?)'
        self.cursor.executemany(query_string, ad_data)


def main():
    params = {
        'db_name': 'ads.db',
        'table_name': 'tractors',
        'category': 'specialtech',
        'min_price': 1000,
        'max_price': 1500,
        }
    rst = Rstua(**params)

    for i in range(1, 50):
        rst.get_page(page_id=i, from_web=True)


if __name__ == "__main__":
    main()
