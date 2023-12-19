from database.database import Database
from discord import Member
from bot import rolesaver

async def save_member(member: Member):
    rolesaver.database.upsert_member(member)

@rolesaver.event
async def on_member_remove(member: Member):
    await save_member(member)
