from service import BaseService
from roles.repository import RoleRepository

class RoleService(BaseService):
    repository = RoleRepository