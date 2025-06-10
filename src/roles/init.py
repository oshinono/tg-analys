from roles.repository import RoleRepository
from roles.schemas import RoleCreate
from sqlalchemy.ext.asyncio import AsyncSession

async def add_user_role_to_db(session: AsyncSession) -> bool:
    data = RoleCreate(name="user", permission_level=0)
    user_role = await RoleRepository.create(data, session=session)
    return user_role is not None


