#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os.path
import urllib.request
import urllib.parse
import json


class Aru():
    MAIN_URL = 'https://auto.ria.com/'
    path_tolistofcars = './listofcars.json'

    def __init__(self, category=4, price_min=0, price_max=0, currency=3,
                 countpage=100):
        self.category = category
        self.price_max = price_max
        self.price_min = price_min
        self.currency = currency
        self.countpage = countpage
        return

    def load_page(self, page=0):
        '''load list of cars from auto.ria.ua by given parameters'''
        params_dict = {
            'price_do': self.price_max,
            'price_ot': self.price_min,
            'currency': self.currency,
            'page': page,
            'category_id': self.category,
            'countpage': self.countpage,
            'bodystyle[2]': 66}

        params = urllib.parse.urlencode(params_dict)
        url = self.MAIN_URL + 'blocks_search_ajax/search/?'
        url += params
        response = urllib.request.urlopen(url)
        content = response.read()
        content = content.decode('utf8')
        with open('./listofcars.json', 'w', encoding='utf-8') as f:
            f.write(content)
        return

    def get_cars_id(self):
        with open(self.path_tolistofcars, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        self.cars_ids = data['result']['search_result']['ids']

    def load_car_info(self, car_id):
        url = self.MAIN_URL + 'demo/bu/searchPage/v2/view/auto/'
        url += car_id
        # maybe delete it?
        url += '/?lang_id=2'
        response = urllib.request.urlopen(url)
        content = response.read()
        content = content.decode('utf8')
        return content


def main():
    tr = Aru(price_min=15000, price_max=45000)
    #tr.load_page()
    tr.get_cars_id()
    # ITERATE LIST OF CARS
    for i in range(1, 10):
        car = tr.load_car_info(tr.cars_ids[i])
        with open('./cartmp', 'w', encoding='utf-8') as f:
            f.write(car)
        with open('./cartmp', 'r', encoding='utf-8') as f:
            car = json.loads(f.read())

        fcar = {}
        fcar['$'] = car['USD']
        fcar['title'] = car['title']
        fcar['Добавлено'] = car['addDate']
        fcar['Модель'] = car['modelName']
        fcar['Марка'] = car['markName']
        fcar['грн'] = car['UAH']
        fcar['url'] = car['linkToView']

        for k, v in fcar.items():
            print(k, v)
        print('+++++++++++++')
    #domain = 'https://auto.ria.com/'
    #response = urllib.request.urlopen(domain + fcar['url'])
    #content = response.read()
    #content = content.decode('utf8')
    #print(content)
    return

if __name__ == "__main__":
    main()
