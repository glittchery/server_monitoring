from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, str_256
from typing import Annotated
import enum
import datetime

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]

class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(50), nullable=false, unique=true)
    password_hash: Mapped[hash] = mapped_column(nullable=false)
    created_at: Mapped[created_at]

class Monitors(Base):
    __tablename__ = "monitors"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    name: Mapped[str] = mapped_column(String(50))
    url: Mapped[str]
    created_at: Mapped[created_at]

class Checks(Base):
    id: Mapped[intpk]
    monitor_id: Mapped[int] = mapped_column(ForeignKey("monitors.id", ondelete="CASCADE"))

    status_code: Mapped[int]
    response_time_ms: Mapped[int]
    success: Mapped[bool]
    checked_at: Mapped[created_at]
    


