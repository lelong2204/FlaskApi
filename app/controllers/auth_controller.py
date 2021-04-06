from flask import Blueprint, request
from flask_jwt_extended import create_access_token
import re
from datetime import timedelta
from app.helper.ultis import custom_response
from app.models.User import User
from mongoengine.errors import DoesNotExist

auth_controller = Blueprint('auth_controller', __name__, url_prefix='/auth')
space = r'\s'


@auth_controller.route("/register", methods=["POST"])
def register():
    try:
        data = request.json
        if "name" not in data.keys() or not data['name'] or data['name'].isspace():
            raise Exception("Missing field name")

        if "username" not in data.keys() or not data['username']:
            raise Exception("Missing field username")

        if re.search(space, data['username']):
            raise Exception("username can not contain white space")

        if "password" not in data.keys() or not data['password']:
            raise Exception("Missing field password")

        if re.search(space, data['password']):
            return "password can not contain white space"

        if len(User.objects(username=data['username'])) != 0:
            raise Exception("Username was exist")
        user = User()
        user.name = data['name']
        user.username = data['username']
        user.password = data['password']
        user.save()

        if user.id is not None:
            return custom_response("Successfully")

        return custom_response("Create new user failed", False)
    except Exception as ex:
        return custom_response(str(ex), False)


@auth_controller.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        if "username" not in data.keys() or not data['username']:
            raise Exception("Missing username")

        if "password" not in data.keys() or not data['password']:
            raise Exception("Missing password")

        user = User.objects.get(username=data['username'])
        auth_status = user.check_pw_hash(data['password'])

        if auth_status:
            token = create_access_token(identity=user, expires_delta=timedelta(hours=24))
            return custom_response("Login Successfully", data={"token": token})

        return custom_response('wrong username or password', False)

    except DoesNotExist:
        return custom_response('wrong username or password', False)

    except Exception as ex:
        return custom_response(str(ex), False)
