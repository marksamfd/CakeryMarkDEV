from app.Repositories.auth_repository import AuthRepository


class AuthService:
    def __init__(self):
        self.auth_repo = AuthRepository()

    # ----------- Add new user -----------
    def add_new_user(self, data):
        return self.auth_repo.add_user(data)

    # ----------- User sign in -----------
    def sign_user_in(self, data):
        return self.auth_repo.user_sign_in(data)
