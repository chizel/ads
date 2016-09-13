#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode, quote
import re
#import os.path
from bs4 import BeautifulSoup


class Olx():
    DOMAIN = 'http://www.olx.ua/'
    CITIES = ('don', 'artemovsk', 'soledar', 'krasnyyliman',
    'kramatorsk', 'slavyansk', 'konstantinovka',
    'lisichansk', 'severodonetsk')

    def __init__(self, query, category='', subcategory='', city='', min_price=0, max_price=0):
        self.make_url(query, category, subcategory, city)

    def make_url(self, query, category, subcategory, city):
        self.url = self.DOMAIN
        if category:
            self.url += category + '/'
            if subcategory:
                self.url += subcategory + '/'
        if city:
            self.url += city + '/'
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
        #ads = s.find_all('td', attrs={'valign': 'top'})
        #ads = s.findAll('td', {'valign': 'top'})
        ads = s.findAll('td', attrs={'class':'offer'})
        #ads = s.find_all('table', attrs={'summary': 'Объявление'})
#        ads = s.find_all('h3', attrs={'class': 'x-large lheight20 margintop5'})
#        title = re.compile('''<strong>(.*)</strong>''')
        re_price = re.compile('''<strong>(.*)</strong>''')
        for ad in ads:
            print(ad)
            exit()
            # extracting image link
            tmp_tag = ad.find('img')
            img_src = tmp_tag['src']
            # extracting ad link 
            # TODO promoted - remove it?
            tmp_tag = ad.find('a', attrs={'class': 'link'})
            ad_link = tmp_tag['href']
            # extracting price
            tmp_tag = ad.find('p', attrs={'class': 'price'})
            price = re_price.search(str(tmp_tag.strong)).group(1)
            # extracting location
            # TODO extract location only
            location = ad.find_all('p', attrs={'class': 'color-9 lheight16 marginbott5'})
            print(location)
            # extracting date
            date = ad.find_all('p', attrs={'class': 'color-9 lheight16 marginbott5 x-normal'})
            print(date)
            #exit()
            #print(ad[:100])
            exit()
        #print(len(ads))


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
