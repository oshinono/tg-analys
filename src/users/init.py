from users.schemas import UserCreate
from roles.schemas import RoleCreate
from sqlalchemy.ext.asyncio import AsyncSession
from roles.service import RoleService
from users.service import UserService
from config import settings
from loguru import logger
import random

async def add_superusers_to_db(session: AsyncSession) -> bool:
    role = await RoleService.get_one_or_none(session=session, name="superuser")
    if not role:
        logger.warning("Роль суперпользователя не найдена, создаю новую")
        role = await RoleService.create(RoleCreate(name="superuser", permission_level=999), session=session)
    
    users = []
    for superuser_tg_id in settings.superuser_tg_ids:
        random_phone_number = f"+79{random.randint(100000000, 999999999)}" # временно, в идеале будет json залетать и там вся инфа о юзерах будет, либо через парсер доставать из таблицы

        data = UserCreate(id=superuser_tg_id, first_name=f"Супер {superuser_tg_id}", phone_number=random_phone_number, role_guid=role.guid)
        try:
            user = await UserService.create(data, session=session)
            users.append(user)
            logger.info(f"Суперпользователь {user.id} добавлен в базу данных")
        except Exception as e:
            logger.error(f"Ошибка при добавлении суперпользователя {superuser_tg_id}: {e}")
            continue
        
    await session.commit()
    return len(users) == len(settings.superuser_tg_ids)