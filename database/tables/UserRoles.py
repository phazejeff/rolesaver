from __future__ import annotations
from sqlalchemy import Table, Column, ForeignKey
from . import Base

userroles = Table(
    "userroles",
    Base.metadata,
    Column("user_id", ForeignKey("Users.id"), primary_key=True),
    Column("role_id", ForeignKey("Roles.id"), primary_key=True)
)