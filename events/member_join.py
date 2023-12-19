from database.database import Database
from discord import Member
from bot import rolesaver

async def restore_member(member: Member):
    user = rolesaver.database.fetch_member(member)
    await member.edit(nick=user.nickname.nickname)
    blacklist = rolesaver.database.fetch_blacklist(member.guild)

    roles = []
    for role in user.roles:
        if (blacklist.is_blacklist and role in blacklist.roles) or (not blacklist.is_blacklist and not role in blacklist.roles):
            continue
        role = member.guild.get_role(role.discord_role_id)
        if role.is_premium_subscriber():
            continue # ignore nitro roles

        if role and not role.is_default():
            roles.append(role)
    
    await member.add_roles(*roles)

@rolesaver.event
async def on_member_join(member: Member):
    await restore_member(member)