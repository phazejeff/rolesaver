import discord
from bot import rolesaver
from commands.forcerestore import attempt_forcerestore

@rolesaver.tree.context_menu(name="Force Restore")
async def forcerestore(interaction: discord.Interaction, member: discord.Member):
    await attempt_forcerestore(interaction, member)