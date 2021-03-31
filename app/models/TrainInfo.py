from mongoengine import Document, StringField, IntField
from mongoengine.base.fields import ObjectIdField


class TrainInfo(Document):
    user_id = ObjectIdField(required=True)
    data_np_path = StringField(max_length=255)
    num_label = IntField(max_value=100, min_value=0)
    label_np_path = StringField(max_length=255)
    data_train_path = StringField(max_length=255)

    def to_json(self):
        return {
            "id": str(self.id),
            "data_np_path": self.data_np_path,
            "label_np_path": self.label_np_path,
            "data_train_path": self.data_train_path,
            "user_id": str(self.user_id),
        }
