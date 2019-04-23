#!/usr/bin/env Python
# coding=utf-8
"""
the url structure of website
"""

from handlers.drawinghandler import DrawingHandler
from handlers.managerhandler import ManagerHandler
url = [
    (r'/', DrawingHandler),
    (r'/manager', ManagerHandler),
]