from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from .Base import Base

class Role(Base):
    __tablename__ = "Roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_server_id: Mapped[int]
    discord_role_id: Mapped[int]

    def __init__(self, discord_server_id: int, discord_role_id: int):
        self.discord_server_id = discord_server_id
        self.discord_role_id = discord_role_id

    def __repr__(self):
        return f"Roles(id={self.id}, discord_server_id={self.discord_server_id}, discord_role_id={self.discord_role_id})"
