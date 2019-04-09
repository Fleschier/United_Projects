import os
import tornado.ioloop
import tornado.websocket
import tornado.web

from tornado.options import options,define

define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

url = [
    (r'/', MainHandler),
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