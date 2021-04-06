from flask import Blueprint, request, current_app
from app.models.Dataset import Dataset
from app.models.Category import Category
from app.helper.ultis import custom_response
from flask_jwt_extended import jwt_required
from mimetypes import guess_extension
from pathlib import Path
import os
import base64
import time

dataset_controller = Blueprint('dataset_controller', __name__, url_prefix='/dataset')


@dataset_controller.route("/add", methods=["POST"])
@jwt_required()
def add_new_dataset():
    try:
        data = request.json
        if "img_base64" not in data.keys() or not data['img_base64'] or data['img_base64'].isspace():
            raise Exception("Image is required")

        if 'base64' not in data['img_base64']:
            raise Exception("Image is not base64")

        if "cate_id" not in data.keys() or not data['cate_id']:
            raise Exception("Category is required")

        data_type = data['img_base64'].split(';base64,')[0]
        img_data = base64.b64decode(data['img_base64'].split(';base64,')[1])
        unix_time = time.time() * 1000000
        cate = Category.objects.get(cate_id=data['cate_id'])
        train_data_folder = current_app.config['train_data_folder']
        img_folder = f'{train_data_folder}/{cate.cate_id}'
        filename = f'{unix_time}{guess_extension(data_type.split(":")[1])}'
        Path(img_folder).mkdir(parents=True, exist_ok=True)

        with open(f'{img_folder}/{filename}', 'wb') as f:
            f.write(img_data)

        dataset = Dataset()
        dataset.name = filename
        dataset.cate_id = data['cate_id']
        dataset.image_url = f'{img_folder}/{filename}'
        dataset.save()

        if dataset.id is not None:
            return custom_response("Successfully", data=dataset.to_json())

        return custom_response("Create new dataset failed", False)
    except Exception as ex:
        return custom_response(str(ex), False)


@dataset_controller.route("/delete/<id>", methods=["POST"])
@jwt_required()
def remove_dataset(id):
    try:
        dataset = Dataset.objects(id=id)
        os.remove(dataset.get().image_url)
        status = dataset.delete()

        if status > 0:
            return custom_response("Successfully")

        return custom_response("Delete dataset failed", False)
    except Exception as ex:
        return custom_response(str(ex), False)
