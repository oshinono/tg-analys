from schemas import BaseCreate, BaseUpdate
from typing import Optional
from roles.enums import Roles

class RoleCreate(BaseCreate):
    name: Roles
    permission_level: int
    

class RoleUpdate(BaseUpdate):
    name: Optional[Roles] = None
    permission_level: Optional[int] = None