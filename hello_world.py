import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from utils.consul_client import ConsulClient
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class HealthChecker(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write("ok")


def main():
    c = ConsulClient('10.20.0.162', '8500')
    service_id = 'Messer' + '10.250.251.23' + ':' + str(10107)
    # print(c.consul.agent.services())

    name = "ms2python"
    address = '10.250.251.23'
    port = 8888
    tags = ['dev']
    interval = 5
    httpcheck = "http://10.250.251.23:8888/actuator/health"
    c.register(name, service_id, address, port, tags, interval, httpcheck)

    tornado.options.parse_command_line()
    application = tornado.web.Application([(r"/", MainHandler), (r"/actuator/health",HealthChecker)])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
