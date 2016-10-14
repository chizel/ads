#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import sqlite3
import os.path
import urllib.request
import urllib.parse
import json


class Aru():
    MAIN_URL = 'https://auto.ria.com/'
    path_tolistofcars = './tmp/listofcars.json'
    DB_NAME = 'tractors.db'

    def __init__(self, category=4, min_price=0, max_price=0, currency=3,
                 countpage=100):
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
        response = urllib.request.urlopen(url)
        content = response.read()
        content = content.decode('utf8')
        with open(self.path_tolistofcars, 'w', encoding='utf-8') as f:
            f.write(content)

    def get_cars_id(self):
        with open(self.path_tolistofcars, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        self.cars_ids = data['result']['search_result']['ids']

    def load_car_info(self, car_id):
        url = self.MAIN_URL + 'demo/bu/searchPage/v2/view/auto/'
        url += car_id
        url += '/?lang_id=2'
        response = urllib.request.urlopen(url)
        content = response.read()
        content = content.decode('utf8')
        return content

    def save_to_db(self, car, car_aru):
        self.cursor.executemany(
            '''INSERT OR IGNORE INTO tractors
            (url, title, uah, usd, added, location, image)
            VALUES (?,?,?,?,?,?,?)''',
            car)
        self.cursor.executemany(
            'INSERT OR IGNORE INTO aru (id, url) VALUES (?,?)', car_aru)

    def get_all_cars(self, save_to_file=False, load_from_file=False):
        self.conn = sqlite3.connect(self.DB_NAME)
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
    tr = Aru(countpage=100, min_price=15000, max_price=45000)
    tr.load_page()
    tr.get_cars_id()
    tr.get_all_cars()


if __name__ == "__main__":
    main()
