#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler
from tornado.escape import to_basestring
from os import path, listdir
from util import load_json


class BaseHandler(RequestHandler):
    def get_current_user(self):
        user = to_basestring(self.get_secure_cookie('user'))
        return user if user and len(user) < 10 else None

    def render(self, template_name, **kwargs):
        kwargs['user'] = self.current_user
        kwargs['uri'] = self.request.uri
        super(BaseHandler, self).render(template_name, **kwargs)


class MainHandler(BaseHandler):
    def get(self):
        pages = sorted([f[:-5] for f in listdir('static/pos') if f.endswith('.json')])
        self.render('index.html', pages=pages)

    def post(self):
        user = self.get_body_argument('user', 0)
        if user:
            self.set_secure_cookie('user', user)
        self.write('ok')


class PageHandler(BaseHandler):
    def get(self, name):
        page = load_json(path.join('static', 'pos', name + '.json'))
        if not page:
            return self.write(name + ' not exist')
        self.render('page.html', page=page)


if __name__ == '__main__':
    app = Application([(r'/', MainHandler), (r'/(\w+)', PageHandler)],
                      debug=True,
                      cookie_secret='R1sl9JqfQnCOS+aAR0fPVPpw5LzQOkzKudChgWnbhKw=',
                      static_path='static',
                      template_path='views')
    app.listen(8001)
    print('Start http://localhost:8001')
    IOLoop.current().start()
