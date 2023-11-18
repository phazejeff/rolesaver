from database.database import Database
from discord import Member

async def _on_member_remove(database: Database, member: Member):
    database.upsert_member(member)