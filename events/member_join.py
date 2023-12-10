from database.database import Database
from discord import Member
from bot import rolesaver

@rolesaver.event()
async def on_member_join(member: Member):
    user = rolesaver.database.fetch_member(member)
    await member.edit(nick=user.nickname.nickname)

    roles = []
    for role in user.roles:
        role = member.guild.get_role(role.discord_role_id)
        if role.is_premium_subscriber():
            continue # ignore nitro roles

        if role and not role.is_default():
            roles.append(role)
    
    await member.add_roles(*roles)