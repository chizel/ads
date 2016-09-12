#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode, quote
import re
#import os.path
from bs4 import BeautifulSoup


class Olx():
    DOMAIN = 'http://www.olx.ua/'
    CITIES = ('artemovsk', 'soledar', 'krasnyyliman',
    'kramatorsk', 'slavyansk', 'konstantinovka',
    'lisichansk', 'severodonetsk')

    def __init__(self, query, category='', subcategory=''):
        self.make_url(query, category, subcategory)

    def make_url(self, query, category, subcategory):
        self.url = self.DOMAIN
        if category:
            self.url += category + '/'
            if subcategory:
                self.url += subcategory + '/'
        self.url += 'q-' + quote(query)

    def get_page(self, page_id=0):
        #response = urlopen(self.url)
        #content = response.read()
        #content = content.decode('utf8')
        #with open('./olxpage.html', 'w', encoding='utf-8') as f:
        #    f.write(content)
        #s = BeautifulSoup(response.read())
        with open('./olxpage.html', 'r') as f:
            s = BeautifulSoup(f.read())
        ads = s.find_all('table', attrs={'summary': 'Объявление'})
        re_price = re.compile('''<strong>(.*)</strong>''')
        for ad in ads:
            print(ad)
            print('+++++++++++++++++++++++++++++')
            # extracting image link
            #tmp_tag = ad.find('img')
            #img_src = tmp_tag['src']
            # extracting ad link 
            #tmp_tag = ad.find('a', attrs={'class': 'link'})
            #ad_link = tmp_tag['href']
            # extracting price
            #tmp_tag = ad.find('p', attrs={'class': 'price'})
            #price = re_price.search(str(tmp_tag.strong)).group(1)
            # extracting location
            location = ad.find_all('p', attrs={'class': 'color-9 lheight16 marginbott5'})
            # extracting date
            date = ad.find_all('p', attrs={'class': 'color-9 lheight16 marginbott5 x-normal'})
            print(t)
            exit()
            #print(ad[:100])
        #print(len(ads))


def main():
    #cat = 'zhivotnye'
    #subcat = 'selskohozyaystvennye-zhivotnye'
    cat = 'transport'
    subcat = ''
    olx = Olx('юмз', cat, subcat)
    olx.get_page()
    return


if __name__ == "__main__":
    main()
