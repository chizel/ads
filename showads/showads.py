#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import web

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/calfs/', 'calfs'
    )


class index:
    def GET(self):
        myvar = {'yt': '%юмз%', 'nt': '%мтз%'}
        db = web.database(dbn='sqlite', db='../ads.db')
        ads = db.select(
            'tractors',
            myvar,
            where='title like $yt and title not like $nt and image != ""',
            order='date(added) desc',
            limit=50)
        return render.index(ads)

class calfs:
    def GET(self):
        db = web.database(dbn='sqlite', db='../ads.db')
        ads = db.select(
            'calfs',
            order='date(added) desc',
            limit=50)
        return render.calfs(ads)


def main():
    return


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()  
