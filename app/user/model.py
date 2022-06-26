from app import db, bcrypt, login_manager
from bson.objectid import ObjectId
import mongoengine as me
from flask_login import UserMixin


class UserCategory(db.EmbeddedDocument):
    id = db.ObjectIdField(default=ObjectId)
    name = db.StringField(required=True, min_length=1, max_length=50)


class Name(db.EmbeddedDocument):
    givenName = db.StringField(required=True, min_length=1, max_length=20)
    surName = db.StringField(required=True, min_length=1, max_length=20)


class User(UserMixin, db.Document):
    username = db.StringField(required=True, unique=True, min_length=4, max_length=20)
    password = db.StringField(required=True, min_length=12, max_length=60)
    category = db.EmbeddedDocumentField(UserCategory, required=True)
    name = db.EmbeddedDocumentField(Name, required=True)
    email = db.EmailField(required=True, unique=True, max_length=50)

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        encrypted = bcrypt.generate_password_hash(document["password"]).decode("utf-8")
        document["password"] = encrypted

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(id):
    return User.objects(id=id).first()


me.signals.pre_save.connect(User.pre_save, sender=User)
