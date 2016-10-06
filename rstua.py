#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import datetime
import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup


class Rstua():
    DOMAIN = 'http://rst.ua/oldcars/'
    DB_NAME = 'dbarucars.db'

    def __init__(self, category, min_price=0, max_price=0):
        self.make_url(category, min_price, max_price)

    def make_url(self, category, min_price, max_price):
        self.url = self.DOMAIN
        self.url += category + '/?'

        if min_price:
            self.url += 'price[]=' + str(min_price) + '&'
        if max_price:
            self.url += 'price[]=' + str(max_price) + '&'

    def get_page(self, page_id=1, from_web=True):
        if from_web:
            response = urlopen(self.url + 'start=' + str(page_id))
            content = response.read()
            content = content.decode('windows-1251')
            with open('./pagerst.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print('Loading page:', page_id)
            s = BeautifulSoup(content)
        else:
            with open('./pagerst.html', 'r') as f:
                s = BeautifulSoup(f.read())

        # connecting to db
        conn = sqlite3.connect(self.DB_NAME)
        self.cursor = conn.cursor()

        ad_data = []
        ads = s.findAll('div', attrs={'class': 'rst-ocb-i '})

        for ad in ads:
            tmp_tag = ad.find('a')
            url = 'http://rst.ua'
            url += tmp_tag['href']

            # check if ad in the db
            item_exists = self.cursor.execute(
                'select count(*) from rstcars where url=?',
                (url,)
                )

            if self.cursor.fetchone()[0]:
                continue

            title = tmp_tag.span.contents[0]
            title = title.lower()
            image_link = tmp_tag.img['src']

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
            #print([title, url, uah, location, image_link])
            ad_data.append([title, url, uah, ad_date, location, image_link])
        self.save_to_db(ad_data)
        conn.commit()
        conn.close()

    def make_date(self, sdate):
        date_info = sdate.split()
        if len(date_info) < 2:
            return datetime.date.today()
        d, m, y = date_info[1].split('.')
        return y + '-' + m + '-' + d

    def save_to_db(self, ad_data):
        #create table rstcars (title char, url char primary key unique,
               # uah int, added datetime, location char, image_link char);
        self.cursor.executemany(
            'INSERT INTO rstcars VALUES (?,?,?,?,?,?)',
            ad_data)


def main():
    params = {
        'category': 'specialtech',
        'min_price': 500,
        'max_price': 2000,
        }
    rst = Rstua(**params)

    for i in range(1, 100):
        rst.get_page(page_id=i, from_web=True)


if __name__ == "__main__":
    main()
