from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from datetime import datetime
from utils import TimestampType

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)

    views_count: Mapped[int] = mapped_column()
    reactions_count: Mapped[int] = mapped_column()
    comments_count: Mapped[int] = mapped_column()
    reposts_count: Mapped[int] = mapped_column()
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"), nullable=False)

    date: Mapped[datetime] = mapped_column(TimestampType, nullable=False)
    is_used: Mapped[bool] = mapped_column(default=False)