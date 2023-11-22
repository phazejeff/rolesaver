from __future__ import annotations
from sqlalchemy import Table, Column, ForeignKey
from .Base import Base

blacklistroles = Table(
    "blacklistroles",
    Base.metadata,
    Column("blacklist_id", ForeignKey("Blacklists.id"), primary_key=True),
    Column("role_id", ForeignKey("Roles.id"), primary_key=True)
)