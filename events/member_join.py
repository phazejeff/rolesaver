from database.database import Database
from discord import Member

async def _on_member_join(database: Database, member: Member):
    user = database.fetch_member(member)

    roles = []
    for role in user.roles:
        role = member.guild.get_role(role.discord_role_id)
        if role.is_premium_subscriber():
            continue # ignore nitro roles

        if role and not role.is_default():
            roles.append(role)
    
    await member.add_roles(*roles)