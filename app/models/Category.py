from mongoengine import Document, StringField, DateTimeField
from mongoengine.base.fields import ObjectIdField

class Category(Document):
    cate_name = StringField(max_length=255, required=True)
    user_id = ObjectIdField(required=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def to_json(self):
        return {
            "id": str(self.id),
            "cate_name": self.cate_name,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }