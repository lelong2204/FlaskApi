from mongoengine import Document, StringField, IntField, DateTimeField
from flask_bcrypt import generate_password_hash, check_password_hash

class User(Document):
    name = StringField(max_length=255, required=True)
    username = StringField(max_length=60, required=True, unique=True)
    email = StringField(max_length=255)
    password = StringField(max_length=100, required=True)
    status = IntField()
    remember_token = StringField(max_length=100)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def to_json(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "status": self.status,
            "remember_token": self.remember_token,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def generate_pw_hash(self):
        self.password = generate_password_hash(password=self.password).decode('utf-8')

    generate_pw_hash.__doc__ = generate_password_hash.__doc__

    def check_pw_hash(self, password):
        return check_password_hash(pw_hash=self.password, password=password)

    def save(self):
        self.generate_pw_hash()
        super(User, self).save()