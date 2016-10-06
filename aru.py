#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3
import os.path
import urllib.request
import urllib.parse
import json


#*********TODO**************************
# add date ad was fetched from the site
#***************************************


class Aru():
    MAIN_URL = 'https://auto.ria.com/'
    path_tolistofcars = './listofcars.json'
    DB_NAME = 'dbarucars.db'

    def __init__(self, category=4, price_min=0, price_max=0, currency=3,
                 countpage=100):
        self.category = category
        self.price_max = price_max
        self.price_min = price_min
        self.currency = currency
        self.countpage = countpage

    def __create_inst__(self):
        #create db
        # Create table
        #query = '
        #create table cars (id int primary key, title char, added datetime,
        #url char, uah int, usd int, brand char, model       char);
        #'
        #c.execute(query)
        pass

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

    def show_car_info(self, car):
        fcar = {}
        fcar['$'] = car['USD']
        fcar['Заголовок'] = car['title']
        fcar['Добавлено'] = car['addDate']
        fcar['Модель'] = car['modelName']
        fcar['Марка'] = car['markName']
        fcar['грн'] = car['UAH']
        fcar['url'] = car['linkToView']
        for k, v in fcar.items():
            print(k, v)
        print('++++++++++++++++++++++++++')

    def save_to_db(self, car):
        self.cursor.executemany(
            'INSERT INTO cars VALUES (?,?,?,?,?,?,?,?)',
            car)

    def get_all_cars(self):
        self.conn = sqlite3.connect(self.DB_NAME)
        self.cursor = self.conn.cursor()
        cars_list = []
        for car_id in self.cars_ids:
            # check if car in the db
            item_exists = self.cursor.execute(
                'select count(*) from cars where id=?',
                (int(car_id),)
                )
            if self.cursor.fetchone()[0]:
                continue

            print('loading car: ', car_id)
            # car isn't in the db, fetching it from the site
            car_info = self.load_car_info(car_id)

            # save to file
            #with open('./cartmp', 'w', encoding='utf-8') as f:
                #f.write(car_info)
            # loading car from a filе (for testing)
            #with open('./cartmp', 'r', encoding='utf-8') as f:
            #    car = json.loads(f.read())

            car = json.loads(car_info)
            tmp = [car_id,
                   car['title'],
                   car['addDate'],
                   self.MAIN_URL + car['linkToView'],
                   car['UAH'],
                   car['USD'],
                   car['modelName'],
                   car['markName'],
                   #car image
                   #car['seoLinkF'],
                   ]
            cars_list.append(tmp)
        self.save_to_db(cars_list)
        self.conn.commit()
        self.conn.close()
        return


def main():
    tr = Aru(countpage=100, price_min=15000, price_max=45000)
    tr.load_page()
    tr.get_cars_id()
    tr.get_all_cars()


if __name__ == "__main__":
    main()
