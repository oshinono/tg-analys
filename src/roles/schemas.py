from schemas import BaseCreate, BaseUpdate
from typing import Optional

class RoleCreate(BaseCreate):
    name: str
    permission_level: int

class RoleUpdate(BaseUpdate):
    name: Optional[str] = None
    permission_level: Optional[int] = None