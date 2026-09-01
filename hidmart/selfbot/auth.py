from dataclasses import dataclass


@dataclass
class AuthState:
    authenticated: bool = False
    user_id: int = 0
    user_name: str = ""


class Auth:
    def __init__(self):
        self.state = AuthState()

    @property
    def is_authenticated(self):
        return self.state.authenticated

    def set_authenticated(self, user_id=0, user_name=""):
        self.state.authenticated = True
        self.state.user_id = user_id
        self.state.user_name = user_name

    def clear(self):
        self.state = AuthState()