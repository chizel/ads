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
    loaded = True
    i = 1
    params = {
        'category': 'specialtech',
        'min_price': 1000,
        'max_price': 2000, 
        }
    rst = Rstua(**params)

    while loaded:
        loaded = rst.get_page(page_id=i, from_web=True)
        i += 1


if __name__ == "__main__":
    main()
