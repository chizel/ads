#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os.path
import urllib.request
import json

categories = [3..13]

#def load_page(page):
    #'''load data from auto.ria.ua category: tractor, price: less than 40000uah'''
    #url = 'https://auto.ria.com/blocks_search_ajax/search/?category_id=4'
    #url += '&currency=3&countpage=100&bodystyle[2]=66&price_do=40000&page=' + str(page)
    #response = urllib.request.urlopen(url)
    #content = response.read()
    #content = content.decode('utf8')

    #with open('./tmp_riaua', 'w', encoding='utf-8') as f:
        #f.write(content)
    #return


#def get_cars_id():
    #with open('./tmp_riaua','r', encoding='utf-8') as f:
        #data = json.loads(f.read())
    #return data['result']['search_result']['ids']


#def load_car_info(car_id):
    #url = 'https://auto.ria.com/demo/bu/searchPage/v2/view/auto/' + car_id + '/?lang_id=2'
    #response = urllib.request.urlopen(url)
    #content = response.read()
    #content = content.decode('utf8')
    #return content

    
#def main():
    ##load_page(0)
    ##cars_id = get_cars_id()
    ##car = load_car_info(cars_id[1])
    ##with open('./cartmp','w', encoding='utf-8') as f:
    ##    f.write(car)
    #with open('./cartmp','r', encoding='utf-8') as f:
        #car = json.loads(f.read())

    #fcar = {}
    #fcar['$'] = car['USD']
    #fcar['title'] = car['title']
    #fcar['Добавлено'] = car['addDate']
    #fcar['linkToView'] = car['linkToView']
    #fcar['Модель'] = car['modelName']
    #fcar['Марка'] = car['markName']
    #fcar['грн'] = car['UAH']
    #fcar['url'] = car['linkToView']

    ##for k,v in fcar.items():
    ##    print(k , v)
    ##domain = 'https://auto.ria.com/'
    ##response = urllib.request.urlopen(domain + fcar['url'])
    ##content = response.read()
    ##content = content.decode('utf8')
    ##print(content)
    #return

#if __name__ == "__main__":
    #main()
