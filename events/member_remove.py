import time
from discord import Member, TextChannel
from bot import rolesaver

async def save_member(member: Member):
    rolesaver.database.upsert_member(member)

    log = rolesaver.database.fetch_log(member.guild)
    if log.is_logging:
        current = round(time.time())
        channel: TextChannel = member.guild.get_channel_or_thread(log.log_channel)
        if channel is None:
            channel = member.guild.fetch_channel(log.log_channel)
        await channel.send(f"<t:{current}:R> {member.name}'s roles have been saved.")

@rolesaver.event
async def on_member_remove(member: Member):
    await save_member(member)
