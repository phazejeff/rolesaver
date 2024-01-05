from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import BigInteger
from . import Base

class Patreon(Base):
    __tablename__ = "Patreon"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_user_id: Mapped[int] = mapped_column(BigInteger())
    discord_server_id: Mapped[int] = mapped_column(BigInteger(), nullable=True)

    def __init__(self, discord_server_id: int):
        self.discord_server_id = discord_server_id

    def __repr__(self):
        return f"Patreon(id={self.id}, discord_server_id={self.discord_server_id}, discord_user_id={self.discord_user_id})"