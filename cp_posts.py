# coding: utf-8

import os

source_path = "/Users/sensoro/hexoBlog/source/_posts/*"
base_path = "/Users/sensoro/hexoBlog/markdown_hexo/_posts/"
os.system("cp -r {0} {1}".format(source_path, base_path))
