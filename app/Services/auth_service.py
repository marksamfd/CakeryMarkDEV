from app.Repositories.auth_repository import AuthRepository


class AuthService:
    def __init__(self):
        self.auth_repo = AuthRepository()
    # ----------- Add new user -----------
    def add_new_user(self,customer_email,data):
        return self.auth_repo.add_user(customer_email,data)
    # ----------- User sign in -----------
    def sign_user_in(self,customer_email,data):
        return self.auth_repo.user_sign_in(customer_email,data)