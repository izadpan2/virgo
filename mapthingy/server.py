import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado import httpclient
import os
import json
import re
from functools import partial



ROOT = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(ROOT, 'templates')
STATIC_DIR = os.path.join(ROOT, 'static')
GOOGLE_MAPS_KEY = 'AIzaSyB98jqPlqa41_FhMKQJfTU_ZA1aC04pjcs'
APISTACK_KEY = 'abfc98d93414c81cc09e7195a04cbd64'
APISTACK_URL_PATTERN = "http://api.ipstack.com/%(host)s&access_key=%(access_key)s"


class APIHandler(tornado.websocket.WebSocketHandler):
    @classmethod
    def is_hostname(cls, s):
        """
        Should return True if the value is a string ending
        in a period, followed by a number of letters.
        """
        regex = re.compile(
            r'(?:[A-Z](?:[A-Z]{0,61}[A-Z])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)', re.IGNORECASE)

        return len(re.findall(regex, s)) > 0

    async def process_message(self, message):
        msg = json.loads(message)
        if msg['msg'] == 'getPosition':
            self.get_position(msg['payload'])
        elif msg['msg'] == 'getPositions':
            self.get_positions(msg['payload'])
        elif msg['msg'] == 'getPositionsSeq':
            self.get_positions_seq(msg['payload'])
        elif msg['msg'] == 'getPositionsAsync':
            await self.get_positions_async(msg['payload'])

    def open(self):
        print("Client connected")

    async def on_message(self, message):
        await self.process_message(message)

    def on_close(self):
        print("WebSocket closed")

    @staticmethod
    def get_api_request_url(host):
        return APISTACK_URL_PATTERN % {'host': host, 'access_key': APISTACK_KEY}

    def get_position(self, host_or_ip):
        client = httpclient.HTTPClient()
        api_request_url = self.get_api_request_url(host_or_ip)
        res = client.fetch(api_request_url)
        self.write_message({
            'msg': 'position',
            'payload': res.body.decode('utf-8'),
            'title': host_or_ip
        })

    def get_positions_seq(self, hosts_or_ips):
        for host in hosts_or_ips:
            self.get_position(host)

    def handle_response(self, host_or_ip, res ):
        self.write_message({
            'msg': 'position',
            'payload': res.body.decode('utf-8'),
            'filter': host_or_ip
        })

    async def get_positions_async(self, hosts_or_ips):
        for host in hosts_or_ips:
            await self.get_position_async(host)

    async def get_position_async(self, host_or_ip):
        client = httpclient.AsyncHTTPClient()
        api_request_url = self.get_api_request_url(host_or_ip)
        await client.fetch(api_request_url, partial(self.handle_response, host_or_ip))

    def get_positions(self, host_or_ip):
        client = httpclient.HTTPClient()
        api_request_url = self.get_api_request_url(host_or_ip)
        res = client.fetch(api_request_url)
        self.write_message({
            'msg': 'position',
            'payload': res.body.decode('utf-8'),
            'title': host_or_ip
        })


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("main.html", google_maps_key=GOOGLE_MAPS_KEY)


def make_app():
    settings = {
        'debug': True,
        'template_path': TEMPLATE_DIR
    }
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/wsapi/", APIHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': STATIC_DIR})
        ], **settings
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
