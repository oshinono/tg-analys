from repository import BaseRepository
from roles.models import Role

class RoleRepository(BaseRepository):
    model = Role