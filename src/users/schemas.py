from schemas import BaseCreate, BaseUpdate
from typing import Optional
import uuid

class UserCreate(BaseCreate):
    id: int
    first_name: str
    username: Optional[str] = None
    phone_number: str
    role_guid: uuid.UUID

class UserUpdate(BaseUpdate):
    id: Optional[int] = None
    first_name: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    role_guid: Optional[uuid.UUID] = None