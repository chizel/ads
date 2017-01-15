#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os.path
import urllib.error
import urllib.parse
import urllib.request
import json


class Aru():
    MAIN_URL = 'https://auto.ria.com/'
    path_tolistofcars = './tmp/listofcars.json'

    def __init__(self, db_name, table_name,
                 category=4, min_price=0, max_price=0,
                 currency=3, countpage=100):
        self.db_name = db_name
        self.table_name = table_name
        self.category = category
        self.max_price = max_price
        self.min_price = min_price
        self.currency = currency
        self.countpage = countpage

    def load_page(self, page=0):
        '''load list of cars from auto.ria.ua by given parameters'''
        params_dict = {
            'price_do': self.max_price,
            'price_ot': self.min_price,
            'currency': self.currency,
            'page': page,
            'category_id': self.category,
            'countpage': self.countpage,
            'bodystyle[2]': 66}

        params = urllib.parse.urlencode(params_dict)
        url = self.MAIN_URL + 'blocks_search_ajax/search/?'
        url += params

        try:
            response = urllib.request.urlopen(url)
            content = response.read()
            content = content.decode('utf8')
            with open(self.path_tolistofcars, 'w', encoding='utf-8') as f:
                f.write(content)
        except urllib.error.HTTPError as e:
            print('Error! %s' % e)
            # we don't get list of cars, nothing to do here
            exit()

    def get_cars_id(self):
        with open(self.path_tolistofcars, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        self.cars_ids = data['result']['search_result']['ids']

    def load_car_info(self, car_id):
        url = self.MAIN_URL + 'demo/bu/searchPage/v2/view/auto/'

        tmp = int(car_id[:-4])
        digit = int(car_id[-4:-3])

        if digit > 4:
            tmp += 1

        tmp = str(tmp)
        url += tmp + '/'
        tmp = int(car_id[:-2])
        digit = int(car_id[-2:-1])

        if digit > 4:
            tmp += 1

        tmp = str(tmp)
        url += tmp + '/'
        url += car_id
        url += '/?lang_id=2'

        try:
            response = urllib.request.urlopen(url)
            content = response.read()
            content = content.decode('utf8')
            return content
        except urllib.error.HTTPError as e:
            print('Error! %s' % e)
        return None

    def save_to_db(self, cars, car_aru):
        query_string = 'INSERT OR IGNORE INTO '
        query_string += self.table_name
        query_string += '(url, title, uah, usd, added, location, image)'
        query_string += 'VALUES (?,?,?,?,?,?,?)'
        self.cursor.executemany(query_string, cars)

        # index table for auto.ria.ua
        self.cursor.executemany(
            'INSERT OR IGNORE INTO aru (id, url) VALUES (?,?)', car_aru)

    def get_all_cars(self, save_to_file=False, load_from_file=False):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        cars = []
        cars_aru = []

        for car_id in self.cars_ids:
            # check if car in the db
            item_exists = self.cursor.execute(
                'SELECT COUNT(*) FROM aru WHERE id=?',
                (car_id,)
                )
            if self.cursor.fetchone()[0]:
                continue

            print('loading car: ', car_id)
            # car isn't in the db, fetching it from the site

            if save_to_file:
                # save to a file
                with open('./cartmp', 'w', encoding='utf-8') as f:
                    f.write(car_info)

            if load_from_file:
                # loading car from a filе (for testing)
                with open('./cartmp', 'r', encoding='utf-8') as f:
                    car = json.loads(f.read())
            else:
                car_info = self.load_car_info(car_id)
                if not car_info:
                    print('Car ' + car_id + ' isn\'t loaded!')
                    continue
                car = json.loads(car_info)

            url = self.MAIN_URL + car['linkToView'][1:]

            tmp = [
                url,
                car['title'].lower(),
                car['UAH'],
                car['USD'],
                car['addDate'],
                car['stateData']['regionName'],
                car['photoData']['seoLinkF'],
                #car['modelName'],
                #car['markName'],
                ]
            cars.append(tmp)
            cars_aru.append([car_id, url])
        self.save_to_db(cars, cars_aru)
        self.conn.commit()
        self.conn.close()


def main():
    # auto.ria.ua
    params = {
        'db_name': 'ads.db',
        'table_name': 'tractors',
        'countpage': 100,
        'min_price': 20000,
        'max_price': 40000,
        }
    tr = Aru(**params)
    tr.load_page()
    tr.get_cars_id()
    tr.get_all_cars()


if __name__ == "__main__":
    main()
