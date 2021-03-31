from datetime import timedelta
from flask import Flask, session, request
from app.controllers import cate_controller
from app.controllers import auth_controller
from app.helper.ultis import response
import json
import os

app = Flask(__name__, template_folder='templates')
with open(os.getcwd() + '/app/config/config.json') as config_file:
	default_config = json.load(config_file)


def main(config: dict = None):
	from flask_mongoengine import MongoEngine

	app.secret_key = "flask demo app"
	app.config.update(default_config)
	db = MongoEngine(app)

	@app.before_request
	def make_session_permanent():
		uncheck_before_request_pages = default_config['uncheck_before_request_pages']
		session.permanent = True
		app.permanent_session_lifetime = timedelta(hours=3)
		if 'Authorization' not in request.headers and request.endpoint not in uncheck_before_request_pages:
			return response(msg="Unauthorized", status=False, code=401), 401

	app.register_blueprint(cate_controller.cate_controller)
	app.register_blueprint(auth_controller.auth_controller)
	app.run(debug=True, port=1234)


if __name__ == "__main__":
	main()
