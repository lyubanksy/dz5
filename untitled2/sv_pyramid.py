from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import pyramid.httpexceptions as exc
import os

from pyramid.wsgi import wsgiapp

middleware_top = "<div class='top'>Middleware TOP</div>"
middleware_bottom =  "<div class='botton'>Middleware BOTTOM</div>"

@wsgiapp
def index(environ, start_response):
    status = '200 OK'
    response_headers = [("Content-Type", "text/html")]
    result = []
    file = open('./index.html','rb')
    for x in file:
    	result.append(x)
    start_response(status, response_headers)
    return result
@wsgiapp
def aboutme(environ, start_response):
    status = '200 OK'
    response_headers = [("Content-Type", "text/html")]
    result = []
    file = open('./about/aboutme.html','rb')
    for x in file:
    	result.append(x)
    start_response(status, response_headers)
    return result

class MiddleWare(object):
 	def __init__(self, app):
 		self.app = app

 	def __call__(self, environ, start_response):
	 	openBody = -1
 		closeBody = -1
 		response = self.app(environ, start_response)
 		for x in response:
 			if "<body>" in x.decode():
	 			openBody = response.index(x)
 			if "</body>" in x.decode():
 				closeBody = response.index(x)
 		result = response[:openBody] + [middleware_top.encode()] + response[openBody:closeBody+1] + [middleware_bottom.encode()] + response[closeBody+1:]
 		return result

if __name__ == '__main__':
    configurator = Configurator()
    configurator.add_route('root', '/')
    configurator.add_view(index, route_name='root')
    configurator.add_route('index_html', '/index.html')
    configurator.add_view(index, route_name='index_html')
    configurator.add_route('aboutme_html', '/about/aboutme.html')
    configurator.add_view(aboutme, route_name='aboutme_html')
    app = configurator.make_wsgi_app()
    myApp = MiddleWare(app)
    server = make_server('localhost', 8000, myApp)
    server.serve_forever()