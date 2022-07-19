from marshmallow import fields, Schema

from setup_db import db
from dao.model.genre import Genre


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String)
    role = db.Column(db.String)
    email = db.Column(db.String)
    surname = db.Column(db.String)
    name = db.Column(db.String)
    favorite_genre = db.Column('favorite_genre', db.Integer, db.ForeignKey('genre.id'))


class UserSchema(Schema):
    id = fields.Int()
    role = fields.Str()
    email = fields.Str()
    surname = fields.Str()
    name = fields.Str()
    favorite_genre = fields.Int()

