from mongoengine import Document, StringField
from mongoengine.base.fields import ObjectIdField

class Dataset(Document):
    name = StringField(max_length=255, required=True)
    cate_id = ObjectIdField(required=True)
    image_url = StringField(max_length=300, required=True)

    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "cate_id": str(self.cate_id),
            "image_url": self.image_url,
        }