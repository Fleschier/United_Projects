import os
import sys
import tornado.ioloop
import tornado.web
import tornado.websocket
import json

from tornado.options import define, options

record = {}
record["clients_hst"] = {
    "clients":set(),
    "handlers":set(),
    "history":{         #存储用户聊天历史记录
        "Demo User":{       
            "Messages":[        # 记录该用户所有收到的历史消息
                ("sender","content")      # 一条记录
            ]
        }
    
    }
}
record["rooms"] = {         #记录房间信息,默认初始一个房间
    "System Default":{
        "description":"default room",
        "members":set(),
        "creater":"System"
    }
}


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
    @tornado.web.authenticated      #装饰器,如果用户调用此方法用户没有登录则会被重定向到登录界面
    def get(self):
        name = tornado.escape.xhtml_escape(self.current_user)
        # self.write("Hey there! " + name)

        userNum = len(record["clients_hst"]["clients"])     #在线人数
        users = record["clients_hst"]["clients"]            #在线所有人名
        roomNum = len(record["rooms"])
        currentRooms = record["rooms"]

        self.render("index.html", name=name, currentNum=userNum, userNames=users, roomNum=roomNum, currentRooms=currentRooms)



class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    
    def post(self):
        userName = self.get_argument("name")

        self.set_secure_cookie("user",userName)         #记录当前用户

        record["clients_hst"]["clients"].add(userName)  #新增用户
        self.redirect("/")

class LogOutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect("/")
        return 

    def post(self):
        userName = tornado.escape.xhtml_escape(self.current_user)
        if userName in record["clients_hst"]["clients"]:
            record["clients_hst"]["clients"].remove(userName)
        for c in record["clients_hst"]["handlers"]:
            if c.userName == userName:
                record["clients_hst"]["handlers"].remove(c)
                break

        self.clear_all_cookies()
        self.redirect("/")

class CreateRoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect("/")

    @tornado.web.authenticated
    def post(self):
        roomName = self.get_argument("roomName")
        descp = self.get_argument("description")
        creater = tornado.escape.xhtml_escape(self.current_user)

        record["rooms"][roomName] = {   #将新的房间信息加入到record中
            "description":descp,
            "members":set(),
            "creater":creater
        }

        self.redirect("/")
        return 

class QuitRoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        roomName = self.get_argument("roomName")
        #currentUser = tornado.escape.xhtml_escape(self.current_user)
        currentUser = self.get_argument("userName")
        if currentUser in record["rooms"][roomName]["members"]:
            record["rooms"][roomName]["members"].remove(currentUser)

        self.set_secure_cookie("user",currentUser)  #刷新cookie为当前用户,然后重定向
        self.redirect("/")
        return

class DeleteRoomHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        roomName = self.get_argument("roomName")
        currentUser = tornado.escape.xhtml_escape(self.current_user)

        if currentUser != record["rooms"][roomName]["creater"]:
            self.write("You are not the creater!")
            self.redirect("/")
            return
        


        record["rooms"].pop(roomName)
        self.redirect("/")

# 加入房间
class JumpHandler(BaseHandler):
    def get(self):
        # currentUser = tornado.escape.xhtml_escape(self.current_user)
        currentUser = self.get_argument("userName")
        # userNums = len(record["clients_hst"]["clients"])
        # userNames = record["clients_hst"]["clients"]
        currentRoomName = self.get_argument("roomName")    #更新当前房间名称

        if currentUser not in record["rooms"][currentRoomName]["members"]:    #新进成员加入计数
            record["rooms"][currentRoomName]["members"].add(currentUser)

        #记录当前房间的名称
        self.set_secure_cookie("currentRoomName", currentRoomName)

        self.render("chat.html", userName=currentUser, roomName=currentRoomName)
        

def updatelist(roomName):           #更新当前房间用户,并传入前端处理
    # total = len(record["clients_hst"]["handlers"])
    # userlist = []
    # for c in record["clients_hst"]["handlers"]:
    #     userlist.append(c.userName)
    #     # pass
    # msg = {
    # 'type': 'list',
    # 'total': total,
    # 'userlist': userlist,
    # }
    # return msg

    total = len(record["rooms"][roomName]["members"])
    userList = list(record["rooms"][roomName]["members"])
    msg = {
        'type': 'list',
        'total': total,
        'userlist': userList,
    }
    return msg

class ChatHandler(tornado.websocket.WebSocketHandler):
    currentRoomName = ""
    userName = ""

    def check_origin(self, origin):
        return True

    """重写 `on_message` 来处理收到的消息, 使用 `write_message` 来发送消息到客户端.
    你也可以重写 `open` 和 `on_close` 来处理连接打开和关闭这两个动作."""

    def reg(self, userName):
        self.userName = userName
        #print(self.userName, "+++++++++++++++++++++++++++++++")

        if self not in record["clients_hst"]["handlers"]:
            record["clients_hst"]["handlers"].add(self)
        self.sendToAllInside({
            'type': 'sys',
            'userName': 'SYSTEM',
            'message': userName + ' has joined the room (System Message)',
            })
        self.sendToAllInside(updatelist(self.currentRoomName))

        # 连接建立后,则恢复该用户的历史消息
        if userName in record["clients_hst"]["history"].keys():      #如果用户存在历史记录
            for msg in record["clients_hst"]["history"][userName]["Messages"]:
                self.write_message(json.dumps({
                    'type': 'msg',
                    'userName': msg[0],
                    'message': msg[1]
                }))
        

    def sendToAllInside(self, message):     # 参数为dict格式
        for client in record["clients_hst"]["handlers"]:
            if client.userName in record["rooms"][self.currentRoomName]["members"]:
                client.write_message(json.dumps(message))

    def open(self):     # 连接建立
        self.write_message(json.dumps({
            'type': 'sys',
            'userName': 'SYSTEM',
            'message': 'Welcome to Chat Room!',
            }))
        
        # 更新房间号
        self.currentRoomName = bytes.decode(self.get_secure_cookie("currentRoomName"))

    def on_close(self):
        # record["rooms"][self.currentRoomName]["members"].remove(self.userName)
        record["clients_hst"]["handlers"].remove(self)
        self.sendToAllInside({
            'type': 'sys',
            'userName': 'SYSTEM',
            'message': self.userName + ' has left the room'
            })
        self.sendToAllInside(updatelist(self.currentRoomName))

    def on_message(self, message):
        msg = json.loads(message)
        roomMembers = record["rooms"][self.currentRoomName]["members"]
        if msg["type"] == "reg":
            self.reg(msg["userName"])

        elif msg["type"] == "msg":      # 如果收到的是用户发送的信息
            if self.userName not in roomMembers:
                roomMembers.add(self.userName)
                self.reg(msg["userName"])
            
            # 给当前房间的每个用户发送信息
            for client in record["clients_hst"]["handlers"]:
                # print("\n\n",client.userName)
                # print(record["rooms"][self.currentRoomName]["members"],"\n\n\n")
                # 如果在线用户也在当前房间,则发送消息给该用户
                if client.userName in record["rooms"][self.currentRoomName]["members"]:
                    client.write_message(message)

                    # 记录历史消息
                    if client.userName in record["clients_hst"]["history"].keys():
                        record["clients_hst"]["history"][client.userName]["Messages"].append((msg["userName"],msg["message"]))
                    else:
                        record["clients_hst"]["history"][client.userName]={    
                                "Messages":[      
                                (msg["userName"],msg["message"])     
                                ]
                        }
            
        else:
            print("Message Error.")

    def recallHistory(self):
        pass
        

import uuid
import base64
secret_code = base64.b64encode(uuid.uuid4().bytes)  #使用加密的cookie

settings = {
    'debug': True,
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'gzip': True,
    'cookie_secret':secret_code,
    # 'xsrf_cookies':True,
    'login_url':"/login",
}

url = [
    (r'/', MainHandler),
    (r'/login', LoginHandler),
    (r'/logout', LogOutHandler),
    (r'/createroom', CreateRoomHandler),
    (r'/quitroom', QuitRoomHandler),
    (r'/deleteroom', DeleteRoomHandler),
    (r'/rooms', JumpHandler),
    (r'/chat',ChatHandler),
]

define("port", default = 8888, help = "run on the given port", type=int)

def main():
    application = tornado.web.Application(handlers=url, **settings)
    application.listen(options.port)
    print("Development server is running at http://127.0.0.1:%s" % options.port)
    print("Quit the server with Control-C")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

