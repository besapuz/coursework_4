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

    @auth_required
    def patch(self):
        req_json = request.json
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
            user_service.update(req_json, email)
            return "", 204


@user_ns.route('/password/')
class UserView(Resource):
    @auth_required
    def put(self):
        req_json = request.json
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
            password_old = req_json.get("password_old")
            user = user_service.get_by_email(email)
            if user_service.compare_password(password_old, user.password):
                return "Пароль неверный", 200
            password_new = user_service.generate_password(req_json.get("password_new"))
            user_service.update_password(password_new, email)
        return "", 204
