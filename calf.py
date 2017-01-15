#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import datetime
import urllib.parse
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
from olx import Olx


def main():
    db_name = 'ads.db'
    table_name = 'calfs'
    queries = [
        'бычок',
        'бычек',
        'бычка',
        'бык',
        'теленок',
        'телка',
        'телку',
        'телочка',
        'теля',
        'телок'
        ]

    params = {
        'category': 'zhivotnye',
        'subcategory': 'selskohozyaystvennye-zhivotnye',
        'min_price': 400,
        'max_price': 2000,
    }

    #cities = (
        #'artemovsk', 'soledar', 'seversk', 'zvanovka', 'krasnyyliman',
        #'kramatorsk', 'slavyansk', 'konstantinovka',
    #    'lisichansk', 'severodonetsk')

    cities = ('don', 'lug')
    olx = Olx('', db_name, table_name, **params)
    i = 1

    for city in cities:
        for query in queries:
            print(city, query)
            params['city'] = city
            olx.make_url(query, **params)
            olx.get_page(page_id=i, from_web=True)
    return


if __name__ == "__main__":
    main()
