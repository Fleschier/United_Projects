#!/usr/bin/env Python
# coding=utf-8
import tornado.web
import os
from url import url

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    )

application = tornado.web.Application(
    handlers = url,
    **settings
    )