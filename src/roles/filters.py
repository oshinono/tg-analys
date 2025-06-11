from filters import BaseDbFilter
from roles.enums import Roles
from users.service import UserService

class AccessFilter(BaseDbFilter):
    def __init__(self, role: Roles):
        self._role = role

    async def __call__(self, event) -> bool:
        user_id: int = event.from_user.id
        user = await UserService.get_by_id(user_id, await self._get_session())
        if not user:
            return False
        
        return user.role.name == self._role.name or user.role.permission_level >= self._role.permission_level
