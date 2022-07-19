import jwt
from flask import request, abort
from flask_restx import Resource, Namespace

from constants import JWT_SECRET
from dao.model.user import UserSchema
from decorators import auth_required, admin_required
from implemented import user_service, auth_service

user_ns = Namespace('user')


@user_ns.route('/')
class UserView(Resource):
    @auth_required
    def get(self):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        try:
            user_decode = jwt.decode(token, JWT_SECRET, algorithms="HS256")
            email = user_decode.get("email")
        except Exception as e:
            print(f"JWT decode {e}")
            abort(401)
        else:
            rs = user_service.get_one(email)
            res = UserSchema(many=True).dump(rs)
            return res, 200


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @auth_required
    def get(self, uid):
        r = user_service.get_one(uid)
        sm_d = UserSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204

    @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
