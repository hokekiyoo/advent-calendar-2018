# coding:utf-8
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import time
import os
from thermometer import read_temp
 
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket Opened")
        self.temps = []
 
    def on_message(self, message):
        print("Message Received")
        while True:
            temp = read_temp()
            self.temps.append(temp)
            n_temp = len(self.temps)
            if n_temp > 12:
                self.temps = self.temps[1:]
            payload = {"temp":self.temps}
            message = json.dumps(payload)
            self.write_message(message)
            print(temp)
            time.sleep(5) #難病に一回データを取るか
            
    def on_close(self):
        print("WebSocket Closed")
        return 0

class MainHandler(tornado.web.RequestHandler):
    def get(self):  
        self.render('index.html')
 
application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", WebSocketHandler),
    ],
    template_path=os.path.join(os.getcwd(), "templates"),
    static_path=os.path.join(os.getcwd(), "static")
)
 
if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.current().start()
