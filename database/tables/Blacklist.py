from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import BigInteger
from typing import Set
from .Base import Base 
from .Roles import Role 
from .BlacklistRoles import blacklistroles

class Blacklist(Base):
    __tablename__ = "Blacklists"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_server_id: Mapped[int] = mapped_column(BigInteger())
    is_blacklist: Mapped[bool] = mapped_column(default=True)
    roles: Mapped[Set[Role] | None] = relationship(secondary=blacklistroles, lazy='subquery')

    def __init__(self, discord_server_id: int):
        self.discord_server_id = discord_server_id
        self.is_blacklist = True

    def __repr__(self):
        return f"Blacklist(id={self.id}, discord_server_id={self.discord_server_id}, is_blacklist={self.is_blacklist}, roles={self.roles})"