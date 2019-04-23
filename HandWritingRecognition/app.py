import os
import tornado.ioloop
import tornado.websocket
import tornado.web
import json
import numpy as np
import mnist_train as mt
import tensorflow as tf

from tornado.options import options,define

define("port", default=8888, help="run on the given port", type=int)

res = 0

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WSHandler(tornado.websocket.WebSocketHandler):
    """重写 `on_message` 来处理收到的消息, 使用 `write_message` 来发送消息到客户端.
    你也可以重写 `open` 和 `on_close` 来处理连接打开和关闭这两个动作."""
    def open(self):
        print("Websocket connected!")

    def on_close(self):
        print("connection closed!")

    def on_message(self, Msg):
        msg = json.loads(Msg)
        # print(msg)
        imgArr = msg["image"].split(",")
        rgba_img = np.array(imgArr).reshape(28,28,4).astype('uint8')
        rgba_img = rgba_img[:,:,3].reshape(1,28,28,1)

        # 调用tensorflow识别返回结果
        res = mt.judge(rgba_img)
        # 将识别结果写回前端
        self.write_message(str(res))
        

url = [
    (r'/', MainHandler),
    (r'/ws',WSHandler),
    ]

settings = {
    'debug': True,
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}

def main():
    application = tornado.web.Application(handlers=url, **settings)
    application.listen(options.port)
    print("Development server is running at http://127.0.0.1:%s" % options.port)
    print("Quit the server with Control-C")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()