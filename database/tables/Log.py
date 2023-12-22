from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger
from .Base import Base 

class Log(Base):
    __tablename__ = "Log"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_server_id: Mapped[int] = mapped_column(BigInteger())
    is_logging: Mapped[bool] = mapped_column(default=False)
    log_channel: Mapped[int | None] = mapped_column(BigInteger(), nullable=True)

    def __init__(self, discord_server_id: int):
        self.discord_server_id = discord_server_id
        self.is_logging = False

    def __repr__(self):
        return f"Log(id={self.id}, discord_server_id={self.discord_server_id}, is_logging={self.is_logging}, log_channel={self.log_channel})"