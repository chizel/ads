#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from olx import Olx
from rstua import Rstua
from aru import Aru


def main():
    params = {
        'db_name': 'ads.db',
        'table_name': 'tractors',
        'min_price': 20000,
        'max_price': 40000,
        #'currency': 'uah',
    }

    # auto.ria.ua
    tr = Aru(countpage=100, **params)
    tr.load_page()
    tr.get_cars_id()
    tr.get_all_cars()

    # olx.ua
    query = 'юмз'
    params['category'] = 'transport'
    olx = Olx(query, **params)
    for i in range(1, 10):
        resp = olx.get_page(page_id=i, from_web=True)
        if resp == 'Redirect':
            break

    # rst.ua
    loaded = True
    i = 1
    params['category'] = 'specialtech'
    params['min_price'] = 900
    params['max_price'] = 1500
    rst = Rstua(**params)

    while loaded:
        loaded = rst.get_page(page_id=i, from_web=True)
        i += 1


if __name__ == "__main__":
    main()
