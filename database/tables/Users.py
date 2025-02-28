from __future__ import annotations
from typing import Set
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.types import BigInteger
from .Roles import Role
from .Base import Base
from .Nickname import Nickname
from .UserRoles import userroles
from .UserNickname import usernicknames

class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_id: Mapped[int] = mapped_column(BigInteger())

    nickname: Mapped[Nickname | None] = relationship(secondary=usernicknames, lazy='subquery') 
    roles: Mapped[Set[Role] | None] = relationship(secondary=userroles, lazy='subquery')

    def __init__(self, discord_id: int):
        self.discord_id = discord_id

    def __repr__(self):
        return f"Users(id={self.id}, discord_id={self.discord_id}, roles={self.roles}, nickname={self.nickname})"