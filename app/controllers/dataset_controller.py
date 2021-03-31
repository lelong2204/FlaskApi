from flask import Blueprint, render_template, session, abort

dataset_controller = Blueprint('dataset_controller', __name__, url_prefix='/dataset')


@dataset_controller.route("/")
def test():
	return "test"
