from werkzeug.wrappers import Request, Response, ResponseStream
from flask import session


class Middleware:
	def __init__(self, app):
		self.app = app
		self.userName = 'Tony'
		self.password = 'IamIronMan'

	def __call__(self, environ, start_response):
		request = Request(environ)
		print(request)
		print(environ)
		print(start_response)
		if request.authorization is not None:
			user_name = request.authorization['username']
			password = request.authorization['password']
			if user_name == self.userName and password == self.password:
				environ['user'] = {'name': 'Tony'}
				return self.app(environ, start_response)

		res = Response(u'Authorization failed', mimetype='application/json', status=401)
		return res(environ, start_response)
