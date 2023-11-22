from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger, VARCHAR
from .Base import Base

class Nickname(Base):
    __tablename__ = "Nicknames"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_server_id: Mapped[int] = mapped_column(BigInteger())
    nickname: Mapped[str | None] = mapped_column(VARCHAR(32), nullable=True)

    def __init__(self, discord_server_id: int, nickname: str):
        self.discord_server_id = discord_server_id
        self.nickname = nickname

    def __repr__(self):
        return f"Nickname(id={self.id}, discord_server_id={self.discord_server_id}, nickname={self.nickname})"