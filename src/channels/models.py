from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import types, text, String
from consts import get_created_at_column, get_updated_at_column
from datetime import datetime
from posts.models import Post

class Channel(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    posts: Mapped[list["Post"]] = relationship(lazy="selectin", cascade="all, delete")