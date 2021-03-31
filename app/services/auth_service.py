from app.models.User import User
from flask import session
from mongoengine.errors import DoesNotExist
import re


class AuthService:
	space = r'\s'

	@staticmethod
	def  register_account(request):
		try:
			if "name" not in request.keys() or not request['name'] or request['name'].isspace():
				return False, "Missing field name"

			if "username" not in request.keys() or not request['username']:
				return False, "Missing field username"

			if re.search(AuthService.space, request['username']):
				return False, "username can not contain white space"

			if "password" not in request.keys() or not request['password']:
				return False, "Missing field password"

			if re.search(AuthService.space, request['password']):
				return False, "password can not contain white space"

			if len(User.objects(username=request['username'])) != 0:
				return False, "Username was exist"

			user = User()
			user.name = request['name']
			user.username = request['username']
			user.password = request['password']
			user.save()

			if user.id is not None:
				return True, user.id

			return False

		except:
			return False, 'something wrong'

	@staticmethod
	def login(request):
		try:
			if "username" not in request.keys() or not request['username']:
				return False, "Missing field username", None

			if re.search(AuthService.space, request['username']):
				return False, "username can not contain white space"

			if "password" not in request.keys() or not request['password']:
				return False, "Missing field password", None

			if re.search(AuthService.space, request['password']):
				return False, "password can not contain white space"

			user = User.objects.get(username=request['username'])
			auth_status = user.check_pw_hash(request['password'])

			if auth_status:
				session.clear()
				session['user_id'] = str(user.id)
				session['user_name'] = user.name
				return True, "Login Successfully", user

			return False, 'wrong username or password', None

		except DoesNotExist:
			return False, 'wrong username or password', None

		except:
			return False, 'something wrong', None

	@staticmethod
	def authentication(id):
		try:
			user = User.objects.get(id=id)
			if user is not None:
				return True

			return False
		except DoesNotExist:
			return False

		except:
			return False
