#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado.escape import to_basestring, json_decode
from os import path, listdir
from util import load_json
from controller.layout import Layout


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
        layout = Layout.load_page(page, 0)
        self.render('page.html', page=page, stage=0, chars=layout.generate_chars())

    def post(self, name):
        if not self.current_user:
            return self.send_error(304, reason='请先设置昵称')

        page = load_json(path.join('static', 'pos', name + '.json'))
        chars = json_decode(self.get_body_argument('chars'))
        layout = Layout.load_page(page, 1)
        chars = layout.apply_chars(chars)
        self.render('page.html', page=page, stage=1, chars=chars)
