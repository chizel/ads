#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import re
#import os.path
from bs4 import BeautifulSoup


class Olx():
    DOMAIN = 'olx.ua/'
    CITIES = ('artemovsk', 'soledar', 'krasnyyliman',
    'kramatorsk', 'slavyansk', 'konstantinovka',
    'lisichansk', 'severodonetsk')

    def __init__(self, category, sub_category):
        self.url = self.DOMAIN + category + '/' + sub_category + '/'

    def get_page(page_id):
        #response = urlopen(self.url)
        #s = BeautifulSoup(response.read())
        with open('/home/a/1.html', 'r') as f:
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
    cat = 'zhivotnye'
    sub_cat = 'selskohozyaystvennye-zhivotnye'
    olx = Olx(cat, sub_cat)
    olx.get_page()
    return


if __name__ == "__main__":
    main()

