import json
import tornado.httpserver
import tornado.ioloop
import tornado.web

from controller import *

ctl = Control()

class TmphumHandler(tornado.web.RequestHandler):
    def get(self):
        res = ctl.get_tmphum()
        self.write(res)

class MyHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        print('Got JSON data:', data)
        res = ctl.module(data)
        self.write(res)

if __name__ == '__main__':
    app = tornado.web.Application([
        tornado.web.url(r'/', MyHandler),
        tornado.web.url(r'/tmphum', TmphumHandler)
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    print('Starting server on port 8888')
    tornado.ioloop.IOLoop.instance().start()
