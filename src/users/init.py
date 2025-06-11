from users.schemas import UserCreate
from roles.schemas import RoleCreate
from sqlalchemy.ext.asyncio import AsyncSession
from roles.enums import Roles
from roles.service import RoleService
from users.service import UserService
from config import settings
from loguru import logger
import random

async def add_superusers_to_db(session: AsyncSession) -> bool:
    role = await RoleService.get_one_or_none(session, name=Roles.SUPERUSER)
    if not role:
        logger.warning("Роль суперюзера не найдена, создаю новую...")
        role = await RoleService.create(RoleCreate(name=Roles.SUPERUSER, permission_level=settings.superuser_permission_level), session)
    else:
        logger.info("Роль суперюзера уже существует")

    for superuser_id in settings.superuser_tg_ids:
        user = await UserService.get_by_id(superuser_id, session)
        if not user:
            logger.warning(f"Пользователь с ID {superuser_id} не найден, создаю...")
            user = await UserService.create(UserCreate(id=superuser_id, 
                                                first_name=f"Пользователь {superuser_id}", 
                                                username=f"@super{superuser_id}",
                                                phone_number=f"+79{random.randint(100000000, 999999999)}",
                                                role_guid=role.guid), 
                                            session)
        else:
            logger.info(f"Пользователь с ID {superuser_id} уже существует")
    
    return True
    