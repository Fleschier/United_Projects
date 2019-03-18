#!/usr/bin/env Python
# coding=utf-8

import tornado.web

class InputHandler(tornado.web.RequestHandler):
    def get(self):
        # username = self.get_argument("user")
        # user_infos = mrd.select_table(table="users",column="*",condition="username",value=username)
        self.render("input.html")

    def post(self):

        # 注意,存入cookie的数据只能是字符串,而且不能包含空格.
        first_num = eval(self.get_argument("first1"))
        self.set_cookie("first_1",str(first_num))
        second_num = eval(self.get_argument("second1"))
        self.set_cookie("second_1",str(second_num))
        thrid_num = eval(self.get_argument("third1"))
        self.set_cookie("third_1", str(thrid_num))
        names = self.get_argument("names1")
        
        names = names.split(" ")

        self.set_cookie("res_1","%".join(names))
        
        self.write("数据输入成功!")

# self.set_cookie(self, name, value, domain=None, expires=None, path="/", expires_days=None, **kwargs)
# self.set_cookie('key', 'value', expires=time.time()+900) 设置超时时间为900秒