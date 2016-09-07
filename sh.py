#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode
import re
#import os.path
from bs4 import BeautifulSoup


#class Adv():
    #def __init__(self, max_price=0, min_price=0, sort_by=0):
        #'''set sort_by to 0 to sort advertises by ascend price,
        #to 1 to sort by date'''
        #self.max_price = max_price
        #self.min_price = min_price
        #return

    #def get_page(url):
        #page = urlopen(self.url)
        #return page

    #def save_page(path):
        #try:
            #self.page
        #except NameError:
            #self.get_page(self.url)
        #with open(path, w) as f:
            #f.write(page)


#class Olx():
    #DOMAIN = 'olx.ua/'
    #CITIES = ('artemovsk', 'soledar', 'krasnyyliman',
    #'kramatorsk', 'slavyansk', 'konstantinovka',
    #'lisichansk', 'severodonetsk')

    #def __init__(self, category, sub_category):
        #self.url = self.DOMAIN + category + '/' + sub_category + '/'

    #def get_page(page_id):
        ##response = urlopen(self.url)
        ##s = BeautifulSoup(response.read())
        #with open('/home/a/1.html', 'r') as f:
            #s = BeautifulSoup(f.read())
        #ads = s.find_all('table', attrs={'summary': 'Объявление'})
        #re_price = re.compile('''<strong>(.*)</strong>''')
        #for ad in ads:
            #print(ad)
            #print('+++++++++++++++++++++++++++++')
            ## extracting image link
            ##tmp_tag = ad.find('img')
            ##img_src = tmp_tag['src']
            ## extracting ad link 
            ##tmp_tag = ad.find('a', attrs={'class': 'link'})
            ##ad_link = tmp_tag['href']
            ## extracting price
            ##tmp_tag = ad.find('p', attrs={'class': 'price'})
            ##price = re_price.search(str(tmp_tag.strong)).group(1)
            ## extracting location
            #location = ad.find_all('p', attrs={'class': 'color-9 lheight16 marginbott5'})
            ## extracting date
            #date = ad.find_all('p', attrs={'class': 'color-9 lheight16 marginbott5 x-normal'})
            #print(t)
            #exit()
            ##print(ad[:100])
        ##print(len(ads))


class Aru():
    DOMAIN = 'https://auto.ria.ua/search/?%s'

    def __init__(self, category_id, marka_id, max_price=0, min_price=0, sort_by=0):
        #'''set sort_by to 0 to sort advertises by ascend price,
        #to 1 to sort by date'''
        self.params = {}
        self.params['category_id'] = str(category_id)
        self.params['marka_id'] = str(marka_id)
        self.params['price_ot'] = str(min_price)
        self.params['price_do'] = str(max_price)
        self.generate_url()

    def generate_url(self):
        url = self.DOMAIN

        for k, v in self.params.items():
            url += k + '=' + v + '&'
        self.url = url
        print(url)

    def get_page(self):
        url = 'https://auto.ria.com/blocks_search_ajax/search/?category_id=4&s_yers[0]=0&po_yers[0]=0&currency=1&marka_id[0]=152&model_id[0]=0&countpage=10&page=0&power_name=1&engineVolumeFrom=&engineVolumeTo=&price_do=2000&price_ot=500'
#        headers = '
        #Host: auto.ria.com
        #User-Agent: Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0
        #Accept: application/json, text/javascript, */*; q=0.01
        #Accept-Language: en-US,en;q=0.5
        #Accept-Encoding: gzip, deflate
        #X-Requested-With: XMLHttpRequest
        #Referer: https://auto.ria.com/search/?category_id=4&marka_id=152&model_id=0
        #Cookie: showNewFeatures=7; showNewFinalPage=1; PHPSESSID=ecjo2cf69dgsrjlnbaaqgd1f96; CCC=0%3A0%3A0; lang_code=ru; newdesign=1; last_auto_actual=true; last_auto_id=17821340; last_news_actual=true; last_news_id=228386; ui=1c9e76255e285aaa
        #Connection: keep-alive'

        params = urlencode(self.params)
        response = urlopen(self.url % params)
        content = response.read()
        self.page = content.decode('utf8')

    def save_page(self, path):
        try:
            self.page
        except NameError:
            self.get_page(self.url)
        with open(path, 'w') as f:
            f.write(self.page)


def main():
    #cat = 'zhivotnye'
    #sub_cat = 'selskohozyaystvennye-zhivotnye'
    #olx = Olx(cat, sub_cat)
    #olx.get_page()
    aru = Aru(4, 152)
    aru.get_page()
    aru.save_page('./1.html')
    return


if __name__ == "__main__":
    main()
