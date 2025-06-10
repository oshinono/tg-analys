from database import Base

from sqlalchemy import ForeignKey, text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import uuid
from consts import get_created_at_column, get_updated_at_column

class Prompt(Base):
    __tablename__ = "prompts"

    guid: Mapped[uuid.UUID] = mapped_column(types.Uuid, primary_key=True, server_default=text("gen_random_uuid()"))

    text: Mapped[str] = mapped_column(nullable=False)
    
    parent_guid: Mapped[uuid.UUID] = mapped_column(ForeignKey("prompts.guid"), nullable=True)
    children_prompts: Mapped[list["Prompt"]] = relationship(lazy="selectin", cascade="all, delete")
    
    created_at: Mapped[datetime] = get_created_at_column()
    updated_at: Mapped[datetime] = get_updated_at_column()