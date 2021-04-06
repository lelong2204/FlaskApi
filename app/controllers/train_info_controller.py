from flask import Blueprint, request, current_app, Response
from app.models.Category import Category
from app.models.TrainInfo import TrainInfo
from app.helper.ultis import custom_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from mimetypes import guess_extension
from pathlib import Path
from app.helper.RainService import cnn_train, predict_image_with_cnn, image_to_matrix
import os
import base64
import time

train_info_controller = Blueprint('train_info_controller', __name__, url_prefix='/train')


@train_info_controller.route("/create_numpy_data", methods=["POST"])
@jwt_required()
def create_numpy_data():
    try:
        user = get_jwt_identity()

        cate_list = Category.objects(user_id=user['_id']['$oid'])
        data_np_path, label_np_path, num_label =  image_to_matrix(cate_list)

        train_info = TrainInfo.objects(user_id=user['_id']['$oid']).first()
        if train_info is None:
            train_info = TrainInfo()
            train_info.data_np_path = data_np_path
            train_info.label_np_path = label_np_path
            train_info.num_label = num_label
            train_info.user_id = user['_id']['$oid']
            train_info.save()
        else:
            train_info.data_np_path = data_np_path
            train_info.label_np_path = label_np_path
            train_info.user_id = user['_id']['$oid']
            train_info.save()

        if train_info.id is not None:
            return custom_response("Successfully", data=train_info.to_json())

        return custom_response("Create new numpy data failed", False)
    except Exception as ex:
        return custom_response(str(ex), False)


@train_info_controller.route("/create_train_data", methods=["POST"])
@jwt_required()
def create_train_data():
    try:
        user = get_jwt_identity()
        train_info = TrainInfo.objects(user_id=user['_id']['$oid']).first()
        if train_info is None or os.path.isfile(train_info.data_np_path) is False \
                or os.path.isfile(train_info.label_np_path) is False or train_info.num_label == 0:
            raise Exception("No data to train")

        path = cnn_train(train_info.data_np_path, train_info.label_np_path, train_info.num_label)
        train_info.data_train_path = path
        train_info.save()

        return custom_response("Successfully", data={"train_path": train_info.data_train_path})
    except Exception as ex:
        return custom_response(str(ex), False)


@train_info_controller.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    try:
        data = request.json
        if "img_base64" not in data.keys() or len(data["img_base64"]) == 0:
            raise Exception("Image is required")

        if "base64" not in data["img_base64"]:
            raise Exception("Image is not base 64 format")

        user = get_jwt_identity()
        train_info = TrainInfo.objects(user_id=user['_id']['$oid']).first()
        if train_info is None or train_info.data_train_path is None or train_info.data_train_path == "":
            raise Exception("You need training data before predict")

        data_type = data['img_base64'].split(';base64,')[0]
        img_data = base64.b64decode(data['img_base64'].split(';base64,')[1])
        unix_time = time.time() * 1000000
        train_data_folder = current_app.config['test_data_folder']
        filename = f'{unix_time}{guess_extension(data_type.split(":")[1])}'
        img_path = f'{train_data_folder}/{filename}'
        Path(train_data_folder).mkdir(parents=True, exist_ok=True)

        with open(img_path, 'wb') as f:
            f.write(img_data)

        index = predict_image_with_cnn(img_path, train_info.data_train_path)
        cate = Category.objects(cate_id=index).first()
        os.remove(img_path)
        if cate is None:
            return custom_response("Cannot predict", False)

        return custom_response("Successfully", True, data=cate.cate_name)
    except Exception as ex:
        return custom_response(str(ex), False)
