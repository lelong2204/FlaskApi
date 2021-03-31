from mongoengine import Document, StringField, IntField
from mongoengine.base.fields import ObjectIdField


class Counter(Document):
    counter_id = StringField(unique=True)
    sequence = IntField()
