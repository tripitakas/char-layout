#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Layout(object):

    @staticmethod
    def load_page(page, stage):
        return Layout(page)

    def __init__(self, page):
        self.page = page

    def generate_chars(self):
        return self.page['chars']

    def apply_chars(chars):
        return chars

