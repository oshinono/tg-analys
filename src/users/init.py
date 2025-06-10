from users.models import User
from users.schemas import UserCreate
from roles.schemas import RoleCreate
from sqlalchemy.ext.asyncio import AsyncSession
from users.repository import UserRepository
from roles.repository import RoleRepository
from config import settings
from loguru import logger

async def add_superusers_to_db(session: AsyncSession) -> bool:
    new_role = await RoleRepository.create(RoleCreate(name="superuser", permission_level=999), session=session)
    users = []
    for superuser_tg_id in settings.superuser_tg_ids:
        data = UserCreate(id=superuser_tg_id, first_name=f"Superuser {superuser_tg_id}", phone_number="", role_guid=new_role.guid)
        try:
            user = await UserRepository.create(data, session=session)
            users.append(user)
            logger.info(f"Суперпользователь {user.id} добавлен в базу данных")
        except Exception as e:
            logger.error(f"Ошибка при добавлении суперпользователя {superuser_tg_id}: {e}")
            continue
    return len(users) == len(settings.superuser_tg_ids)