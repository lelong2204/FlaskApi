from flask import Flask, send_from_directory
from app.controllers.cate_controller import cate_controller
from app.controllers.auth_controller import auth_controller
from app.controllers.dataset_controller import dataset_controller
from app.controllers.train_info_controller import train_info_controller
from flask_jwt_extended import JWTManager
import json

app = Flask(__name__, static_url_path='')
with open('config/config.json') as config_file:
	default_config = json.load(config_file)


def main(config: dict = None):
	from flask_mongoengine import MongoEngine

	app.secret_key = "flask demo app"
	app.config.update(default_config)
	jwt = JWTManager(app)
	db = MongoEngine(app)

	@app.route('/img/<path:path>')
	def send_js(path):
		return send_from_directory('img', path)

	app.register_blueprint(cate_controller)
	app.register_blueprint(auth_controller)
	app.register_blueprint(dataset_controller)
	app.register_blueprint(train_info_controller)
	app.run(debug=True, port=1234)


if __name__ == "__main__":
	main()
