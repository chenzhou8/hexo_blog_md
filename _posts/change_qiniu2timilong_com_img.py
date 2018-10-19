# coding: utf-8

import os

base_dir = "/Users/sensoro/hexoBlog/source/_posts"

all_files = os.listdir(base_dir)
files_abspath = [os.path.join(base_dir, item) for item in all_files]
print(files_abspath)

for _f in files_abspath:
    with open(_f, 'w+') as fp:
        md_data = fp.read()
