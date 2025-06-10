from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from consts import get_created_at_column, get_updated_at_column
from datetime import datetime
import uuid
from roles.models import Role

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = get_created_at_column()
    updated_at: Mapped[datetime] = get_updated_at_column()

    role_guid: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.guid"), nullable=False)
    role: Mapped["Role"] = relationship()