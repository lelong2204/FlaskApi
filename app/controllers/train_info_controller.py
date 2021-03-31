from flask import Blueprint, request, current_app
from app.models.Category import Category
from app.models.TrainInfo import TrainInfo
from app.helper.ultis import custom_response
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import base64
from app.helper.RainService import cnn_train, predict_image_with_cnn, image_to_matrix

train_info_controller = Blueprint('train_info_controller', __name__, url_prefix='/train')


@train_info_controller.route("/create_numpy_data", methods=["POST"])
@jwt_required()
def create_numpy_data():
    try:
        user = get_jwt_identity()

        cate_list = Category.objects(user_id=user['_id']['$oid'])
        print(len(cate_list))
        data_np_path, label_np_path, num_label = image_to_matrix(cate_list)

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
        if train_info is None or os.path.isfile(train_info.data_np_path) == False \
                or os.path.isfile(train_info.label_np_path) == False or train_info.num_label == 0:
            raise Exception("No data to train")

        path = cnn_train(train_info.data_np_path, train_info.label_np_path, train_info.num_label)
        train_info.data_train_path = path
        train_info.save()

        return custom_response("Successfully", data={"train_path": train_info.data_train_path})
    except Exception as ex:
        print(ex)
        return custom_response(str(ex), False)
