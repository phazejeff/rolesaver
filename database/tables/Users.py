from __future__ import annotations
from typing import Set
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.types import BigInteger
from .Roles import Role
from .Base import Base
from .UserRoles import userroles

class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_id: Mapped[int] = mapped_column(BigInteger())

    roles: Mapped[Set[Role] | None] = relationship(secondary=userroles)

    def __init__(self, discord_id: int):
        self.discord_id = discord_id

    def __repr__(self):
        return f"Users(id={self.id}, discord_id={self.discord_id}, roles={self.roles})"