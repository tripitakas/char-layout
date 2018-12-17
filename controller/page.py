#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado.escape import to_basestring, json_decode
from os import path, listdir
from util import load_json, save_json
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
        # 用户选择一个页面开始校对，先读取原始列框和字框的切分数据
        page = load_json(path.join('static', 'pos', name + '.json'))
        if not page:
            return self.write(name + ' not exist')

        # 请求字框计算模块生成初始的字框类型（普通字、夹注小字）
        layout = Layout.load_page(page, 0)
        chars = layout.generate_chars()

        self.render('page.html', page=page, stage=0, chars=chars)

    def post(self, name):
        if not self.current_user:
            return self.send_error(304, reason='请先设置昵称')

        filename = path.join('static', 'pos', name + '.json')
        page = load_json(filename)
        stage = int(self.get_body_argument('stage'))
        layout = Layout.load_page(page, stage)

        if stage == 1:
            # 用户校对完字框类型后，请求字框计算模块生成字框顺序
            inline_chars = json_decode(self.get_body_argument('inline_chars', '[]'))
            chars = page['chars']
            assert len(inline_chars) == len(chars)
            for i, c in enumerate(chars):
                c['inline-char'] = inline_chars[i]
            chars = layout.apply_inline_chars(chars)
            self.render('page.html', page=page, stage=stage, chars=chars)

        elif stage == 2:
            # 用户拖拽改变字框顺序，请求字框计算模块生成字框和列框的编号
            chars = json_decode(self.get_body_argument('chars', '[]'))
            assert len(chars) == len(page['chars'])
            if layout.apply_chars_order(chars):
                save_json(page, filename)
                stage = 3
            self.render('page.html', page=page, stage=stage, chars=chars)
