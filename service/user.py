import base64
import hashlib
import hmac

from constants import ALGO, PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDao


class UserService:
    def __init__(self, dao: UserDao):
        self.dao = dao

    # def get_one(self, email):
    #     return self.dao.get_one(email)

    def get_by_email(self, email):
        return self.dao.get_email(email)

    def check_email(self, email):
        return self.dao.get_one(email)

    def create(self, user_d):
        user_d["password"] = self.generate_password(user_d["password"])
        if self.dao.get_email(user_d["email"]):
            return False
        return self.dao.create(user_d)

    def update(self, user_d, email):
        self.dao.update(user_d, email)
        return self.dao

    def update_password(self, user_d, email):
        self.dao.update_password(user_d, email)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)

    def generate_password(self, password):
        hash_digest = base64.b64encode(hashlib.pbkdf2_hmac(
            ALGO,
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )).decode('utf-8')
        return hash_digest

    def compare_password(self, password_hash, other_password):

        hash_digest = base64.b64encode(hashlib.pbkdf2_hmac(
            ALGO,
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )).decode('utf-8')
        return hmac.compare_digest(password_hash, hash_digest)
