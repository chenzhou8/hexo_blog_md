# coding: utf-8

import os

post_source_path = "/Users/sensoro/hexoBlog/source/_posts/*"
post_base_path = "/Users/sensoro/hexoBlog/github_hexo/_posts/"
os.system("rm -rf {0}".format(post_base_path))
os.system("mkdir {0}".format("_posts"))
os.system("cp -r {0} {1}".format(post_source_path, post_base_path))

summary_source_path = "/Users/sensoro/hexoBlog/source/summary/*"
summary_base_path = "/Users/sensoro/hexoBlog/github_hexo/summary/"
os.system("rm -rf {0}".format(summary_base_path))
os.system("mkdir {0}".format("summary"))
os.system("cp -r {0} {1}".format(summary_source_path, summary_base_path))

about_source_path = "/Users/sensoro/hexoBlog/source/about/*"
about_base_path = "/Users/sensoro/hexoBlog/github_hexo/about/"
os.system("rm -rf {0}".format(about_base_path))
os.system("mkdir {0}".format("about"))
os.system("cp -r {0} {1}".format(about_source_path, about_base_path))

os.system("git add . ")
os.system("git commit -m 'update _posts/' ")
os.system("git push origin master")

