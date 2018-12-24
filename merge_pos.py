#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util import load_json, save_json, create_folders
from os import path, listdir, remove
import sys

DST_PATH = path.join(path.dirname(__file__), 'static', 'pos')
indexes = dict(pages={}, kinds={})


def scan_dir(src_paths, dst_path, kind, level):
    exists = [path.exists(p) for p in src_paths]
    if exists != [True, True, True]:
        print('%s: %d %d %d' % tuple(src_paths[:1] + exists))
    if not exists[0]:
        return 0
    create_folders(dst_path)
    count = 0
    for fn in listdir(src_paths[0]):
        dst_file = path.join(dst_path, fn)
        if path.isdir(path.join(src_paths[0], fn)):
            count += scan_dir([path.join(p, fn) for p in src_paths], dst_file,
                              len(fn) == 2 and level == 0 and fn or kind, level + 1)
            if not count and path.exists(dst_file):
                try:
                    remove(dst_file)
                except:
                    pass
        elif fn.endswith('.json') and fn[:2] == kind:
            char, block, column = [load_json(path.join(p, fn)) for p in src_paths]
            if char and char.get('chars') and char['imgname'][:2] == kind:
                char['blocks'] = block and block.get('blocks') or char.get('blocks')
                char['columns'] = column and column.get('columns') or char.get('columns')
                if char['blocks'] and char['columns']:
                    save_json(char, dst_file)
                    count += 1
                    indexes['kinds'][kind] = indexes['kinds'].get(kind, []) + [char['imgname']]
                    indexes['pages'][char['imgname']] = dst_file
    return count


def scan_root_dir(src_path, dst_path):
    scan_dir([path.join(src_path, s) for s in ['char', 'block', 'column']], dst_path, None, 0)


if __name__ == '__main__':
    scan_root_dir(sys.argv[1] if len(sys.argv) > 1 else './pos', DST_PATH)
    save_json(indexes, path.join(path.dirname(__file__), 'static', 'index.json'))
