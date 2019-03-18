import tornado.web
import methods.Util as Util

class ResultHandler(tornado.web.RequestHandler):
    def get(self):
    #     # username = self.get_argument("user")
    #     # user_infos = mrd.select_table(table="users",column="*",condition="username",value=username)
    #     self.render("result.html")
        first_num = eval(self.get_cookie("first_1"))
        second_num = eval(self.get_cookie("second_1"))
        thrid_num = eval(self.get_cookie("third_1"))
        names = self.get_cookie("res_1")

        #将输入的名字切割存入列表
        nameLst = names.split("%")
        #res为随机抽取的结果下标的列表
        res_idx = Util.getRandIdx(len(nameLst), first_num + second_num + thrid_num)
        res = []
        for i in res_idx:
            res.append(nameLst[i])

        print("获奖列表",res)
        self.render("result.html", first=first_num,second=second_num,third=thrid_num,res1=" ".join(res[:first_num]), res2=" ".join(res[first_num:first_num+second_num]),res3=" ".join(res[first_num+second_num:]) )

    # def post(self):
        