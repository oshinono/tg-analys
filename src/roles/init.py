from roles.schemas import RoleCreate
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from roles.service import RoleService

async def add_user_role_to_db(session: AsyncSession) -> bool:
    try:
        data = RoleCreate(name="user", permission_level=0)
        user_role = await RoleService.create(data, session=session)
        return user_role is not None
    except Exception as e:
        logger.error(f"Ошибка при добавлении роли пользователя: {e}")
        return False


