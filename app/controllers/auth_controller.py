from flask import Blueprint, render_template, request, flash
from app.services.auth_service import AuthService

auth_controller = Blueprint('auth_controller', __name__, url_prefix='/auth')


@auth_controller.route("/register", methods=["POST"])
def register():
	register_status, message = AuthService.register_account(request.json)
	if register_status:
		return "resgister done"
	else:
		return message


@auth_controller.route("/login", methods=["POST"])
def login():
	login_status, message, user = AuthService.login(request.json)

	if login_status:
		flash("Login successfully")
		return "login done"
	else:
		return "login fail"