#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.web import RequestHandler
from tornado.escape import to_basestring, json_decode, url_unescape
from util import load_json, save_json

from .layout_demo import main as core

indexes = load_json('static/index.json')


class BaseHandler(RequestHandler):
    def get_current_user(self):
        user = to_basestring(self.get_secure_cookie('user'))
        return user if user and len(user) < 10 else None


class MainHandler(BaseHandler):
    def get(self):
        self.render('index.html', indexes=indexes['kinds'])

    def post(self):
        user = self.get_body_argument('user', 0)
        if user:
            self.set_secure_cookie('user', user)
        self.write('ok')


class PageHandler(BaseHandler):
    def get(self, name):
        # 用户选择一个页面开始校对，先读取原始列框和字框的切分数据
        filename = indexes['pages'].get(name)
        page = load_json(filename)
        if not page:
            return self.write(name + ' not exist')

        # 请求字框计算模块生成初始的字框类型（普通字、夹注小字）
        chars = core.calc(page['chars'], page['blocks'], page['columns'])
        # save_json(chars, '_chars.json')

        self.render('page0.html', page=page, stage=0, chars=chars,
                    img_file=filename.replace('static/pos', 'img').replace('.json', '.jpg'))

    def post(self, name):
        if not self.current_user:
            return self.write('请先设置昵称。')

        page = load_json(indexes['pages'].get(name))
        stage = int(self.get_body_argument('stage'))

        if stage == 0:
            # 用户校对完字框类型后，请求字框计算模块生成字框顺序
            inline_chars = json_decode(self.get_body_argument('chars'))
            chars = page['chars']
            assert len(inline_chars) == len(chars)
            for i, (c, inline) in enumerate(zip(chars, inline_chars)):
                if 'is_small_changed' in inline:
                    c['is_small_changed'] = inline['is_small_changed']
            chars = core.calc(chars, page['blocks'], page['columns'])
            self.render('page1.html', page=page, stage=1, chars=chars)

        elif stage == 1:
            # 用户拖拽改变字框顺序，请求字框计算模块生成字框和列框的编号
            chars = json_decode(self.get_body_argument('chars', '[]'))
            assert len(chars) == len(page['chars'])
            if layout.apply_chars_order(chars):
                save_json(page, filename)
                stage = 3
            self.render('page.html', page=page, stage=stage, chars=chars)
