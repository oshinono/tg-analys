from repository import BaseRepository
from users.models import User

class UserRepository(BaseRepository):
    model = User