from service import BaseService
from users.repository import UserRepository

class UserService(BaseService):
    repository = UserRepository