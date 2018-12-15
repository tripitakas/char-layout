#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from os import path, listdir
from util import load_json


class MainHandler(RequestHandler):
    def get(self):
        pages = sorted([f[:-5] for f in listdir('static/pos') if f.endswith('.json')])
        self.render('index.html', pages=pages)


class PageHandler(RequestHandler):
    def get(self, name):
        page = load_json(path.join('static', 'pos', name + '.json'))
        if not page:
            return self.write(name + ' not exist')
        self.render('page.html', page=page)


if __name__ == '__main__':
    app = Application([(r'/', MainHandler), (r'/(\w+)', PageHandler)],
                      debug=True, static_path='static')
    app.listen(8001)
    print('Start http://localhost:8001')
    IOLoop.current().start()
