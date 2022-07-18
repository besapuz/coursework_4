from marshmallow import fields, Schema

from setup_db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)
    role = db.Column(db.String)
    email = db.Column(db.String)


class UserSchema(Schema):
    id = fields.Int()
    password = fields.Str()
    role = fields.Str()
    email = fields.Str()

