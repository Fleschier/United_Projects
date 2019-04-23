import tornado.web
class DrawingHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("canvas.html")
    def post(self):
        pass