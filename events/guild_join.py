from bot import rolesaver
from discord import Guild

@rolesaver.event
async def on_guild_join(guild: Guild):
    await rolesaver.tree.sync(guild=guild)
