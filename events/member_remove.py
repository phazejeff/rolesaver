from database.database import Database
from discord import Member
from bot import rolesaver

@rolesaver.event()
async def on_member_remove(member: Member):
    rolesaver.database.upsert_member(member)