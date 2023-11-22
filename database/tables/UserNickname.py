from __future__ import annotations
from sqlalchemy import Table, Column, ForeignKey
from . import Base

usernicknames = Table(
    "usernicknames",
    Base.metadata,
    Column("user_id", ForeignKey("Users.id"), primary_key=True),
    Column("nickname_id", ForeignKey("Nicknames.id"), primary_key=True)
)
