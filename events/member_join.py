import time
from discord import Member, TextChannel
from bot import rolesaver
from discord.errors import Forbidden

async def restore_member(member: Member):
    user = rolesaver.database.fetch_member(member)
    print(user)
    if user.nickname != None:
        try:
            await member.edit(nick=user.nickname.nickname)
        except Forbidden:
            pass
    blacklist = rolesaver.database.fetch_blacklist(member.guild)

    roles = []
    for role in user.roles:
        if (blacklist.is_blacklist and role in blacklist.roles) or (not blacklist.is_blacklist and not role in blacklist.roles):
            continue
        role = member.guild.get_role(role.discord_role_id)
        if role == None:
            continue
        if role.is_premium_subscriber():
            continue # ignore nitro roles

        if role and not role.is_default():
            roles.append(role)
    
    try:
        await member.add_roles(*roles, atomic=True)
    except Forbidden:
        log = rolesaver.database.fetch_log(member.guild)
        if log.is_logging:
            current = round(time.time())
            channel: TextChannel = member.guild.get_channel_or_thread(log.log_channel)
            if channel is None:
                channel = await member.guild.fetch_channel(log.log_channel)
            await channel.send(f"<t:{current}:R> {member.name}'s roles failed being restored due to permission issue.")
            return

    log = rolesaver.database.fetch_log(member.guild)
    if log.is_logging:
        current = round(time.time())
        channel: TextChannel = member.guild.get_channel_or_thread(log.log_channel)
        if channel is None:
            channel = await member.guild.fetch_channel(log.log_channel)
        await channel.send(f"<t:{current}:R> {member.name}'s roles have been restored.")

@rolesaver.event
async def on_member_join(member: Member):
    await restore_member(member)