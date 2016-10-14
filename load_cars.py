#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from olx import Olx
from rstua import Rstua
from aru import Aru

def main():
    # auto.ria.ua
    min_price = 20000
    max_price = 45000
    tr = Aru(countpage=100, min_price=min_price, max_price=max_price)
    tr.load_page()
    tr.get_cars_id()
    tr.get_all_cars()

    exit()
    # olx.ua
    query = 'юмз'
    params = {
        'category': 'transport',
        'subcategory': '',
        'min_price': min_price,
        'max_price': max_price,
        #'currency': 'uah',
    }
    olx = Olx(query, **params)
    for i in range(1, 4):
        olx.get_page(page_id=i, from_web=True)

    # rst.ua
    params = {
        'category': 'specialtech',
        'min_price': min_price,
        'max_price': max_price
        }
    rst = Rstua(**params)

    for i in range(1, 100):
        rst.get_page(page_id=i, from_web=True)


if __name__ == "__main__":
    main()
