from sqlalchemy import String, ForeignKey, func, Integer
from sqlalchemy.orm import Mapped, mapped_column
from src.database.database import Base
from typing import Annotated
import datetime
import enum


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.date_trunc("second", func.now()))]

class Users(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str]
    created_at: Mapped[created_at]


class dns_or_https(enum.Enum):
    dns = "dns"
    https = "https"

class Monitors(Base):
    __tablename__ = "monitors"

    id: Mapped[intpk]

    type_of_request: Mapped[dns_or_https]
    name: Mapped[str] = mapped_column(String(50))
    url: Mapped[str]
    interval: Mapped[int]
    next_check_at: Mapped[created_at]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

class Checks(Base):
    __tablename__ = "checks"

    id: Mapped[intpk]

    status_code: Mapped[int] = mapped_column(nullable=True)
    response_time_ms: Mapped[str] = mapped_column(nullable=True)
    success: Mapped[bool]
    reason: Mapped[str]
    created_at: Mapped[created_at]
    monitor_id: Mapped[int] = mapped_column(ForeignKey("monitors.id", ondelete="CASCADE"))


