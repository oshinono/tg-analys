from roles.schemas import RoleCreate
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from roles.service import RoleService
from roles.enums import Roles
from config import settings

async def add_user_role_to_db(session: AsyncSession) -> bool:
    role = await RoleService.get_one_or_none(session, name=Roles.USER)
    if not role:
        logger.warning("Роль юзера не найдена, создаю...")
        role = await RoleService.create(RoleCreate(name=Roles.USER, permission_level=settings.superuser_permission_level), session)
    else:
        logger.info("Роль юзера уже существует")


