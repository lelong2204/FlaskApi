from flask import Blueprint, jsonify
from app.helper.ultis import response

cate_controller = Blueprint('cate_controller', __name__, url_prefix='/cate')


@cate_controller.route("/getall")
def list():
	return response("Get Cate List")
