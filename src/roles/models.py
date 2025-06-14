from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sqlalchemy import types
from datetime import datetime
from sqlalchemy import String, text, CheckConstraint
import uuid
from consts import get_created_at_column, get_updated_at_column

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = (
        CheckConstraint("permission_level >= 0"),
    )

    id: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    permission_level: Mapped[int] = mapped_column(nullable=False, index=True)
    created_at: Mapped[datetime] = get_created_at_column()
    updated_at: Mapped[datetime] = get_updated_at_column()