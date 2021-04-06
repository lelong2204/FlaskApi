from flask import Blueprint, request, current_app
from app.helper.ultis import custom_response
from app.models.Category import Category
from app.models.Counter import Counter
from flask_jwt_extended import jwt_required, get_jwt_identity
from pathlib import Path

cate_controller = Blueprint('cate_controller', __name__, url_prefix='/cate')


@cate_controller.route("/add", methods=["POST"])
@jwt_required()
def add_new_cate():
	try:
		data = request.json
		user = get_jwt_identity()

		if "cate_name" not in data.keys() or not data['cate_name'] or data['cate_name'].isspace():
			raise Exception("Missing field category name")

		counter = Counter.objects(counter_id="cate_id").first()
		if counter is None:
			counter = Counter()
			counter.counter_id = "cate_id"
			counter.sequence = 0
			counter.save()

		cate = Category()
		cate.cate_id = counter.sequence
		cate.cate_name = data['cate_name']
		cate.user_id = user['_id']['$oid']
		cate.save()
		counter.sequence += 1
		counter.save()

		train_data_folder = current_app.config['train_data_folder']
		img_folder = f'{train_data_folder}/{cate.cate_id}'
		Path(img_folder).mkdir(parents=True, exist_ok=True)

		if cate.id is not None:
			return custom_response("Successfully")

		return custom_response("Create new category failed", False)
	except Exception as ex:
		return custom_response(str(ex), False)


@cate_controller.route("/list")
@jwt_required()
def get_all_cate():
	try:
		return custom_response("Successfully", Category.objects)
	except Exception as ex:
		return custom_response(str(ex), False)
