from flask import request, abort
from flask_restx import Resource, Namespace

from implemented import auth_service, user_service

auth_ns = Namespace('auth')


@auth_ns.route('/register/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        c = user_service.create(req_json)
        if not c:
            return "Пользователь существует"
        return "", 201


@auth_ns.route('/login/')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get("email", None)
        password = req_json.get("password", None)

        if None in [email, password]:
            abort(400)
        token = auth_service.generation_token(email, password)
        return token, 201

    def put(self):
        req_json = request.json
        token = req_json.get("refresh_token")
        tokens = auth_service.approve_refresh_token(token)

        return tokens, 201
