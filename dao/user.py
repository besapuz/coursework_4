from dao.model.user import User


class UserDao:
    def __init__(self, session):
        self.session = session

    def get_one(self, email):
        return self.session.query(User).filter(User.email == email).all()

    def get_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def create(self, user_a):
        ent = User(**user_a)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_a, email):
        user = self.get_email(email)
        if 'favorite_genre' in user_a:
            user.favorite_genre = user_a.get('favorite_genre')
        if 'surname' in user_a:
            user.surname = user_a.get('surname')
        if 'name' in user_a:
            user.name = user_a.get('name')

        self.session.add(user)
        self.session.commit()

    def update_password(self, password_new, email):
        user = self.get_email(email)
        user.password = password_new

        self.session.add(user)
        self.session.commit()
