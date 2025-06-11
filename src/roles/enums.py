from enum import Enum
from config import settings

class Roles(str, Enum):
    SMM = "smm", settings.smm_permission_level
    ADMIN = "admin", settings.admin_permission_level
    USER = "user", settings.user_permission_level
    SUPERUSER = "superuser", settings.superuser_permission_level

    def __new__(cls, str_value: str, int_value: int):
        obj = str.__new__(cls, str_value)
        obj._value_ = str_value
        obj.permission_level = int_value  # Дополнительное значение
        return obj