from aiogram import Router
from roles.filters import AccessFilter
from roles.enums import Roles

router = Router()
router.message.filter(AccessFilter(Roles.ADMIN))
router.callback_query.filter(AccessFilter(Roles.ADMIN))
