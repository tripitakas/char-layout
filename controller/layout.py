#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .layout_demo import main as core


class Layout(object):

    @staticmethod
    def load_page(page, stage):
        return Layout(page)

    def __init__(self, page):
        self.page = page

    def generate_chars(self):
        """ 生成初始的字框类型，设置是普通字还是夹注小字，可以不分配字框的char_id """
        # for c in self.page['chars']:
        #     c['inline-char'] = 1 if 是夹注小字 else 0
        return self.page['chars']

    def apply_inline_chars(self, chars):
        """ 校对完夹注小字(改变chars中的inline-char)后，生成字框顺序(对字框排序，设置字框的char_id) """
        return chars

    def apply_chars_order(self, chars):
        """ 校对完字框顺序(chars排序)后，重新设置字框顺序(设置字框的char_id、列框的column_id，可以在page中改) """
        return True
