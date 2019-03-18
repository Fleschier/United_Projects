#coding = utf-8

"""
basic weisite settings
"""

from url import url     #从url.py中引入网站目录结构

import tornado.web
import os

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),        #注意这里static目录绝对不要加s!!
    debug = True        #服务器不重启就可以看到修改代码的效果
)

application = tornado.web.Application(
    handlers = url,
    **settings
)