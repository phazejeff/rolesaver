import discord
from bot import rolesaver
from commands.forcesave import attempt_forcesave

@rolesaver.tree.context_menu(name="Force Save")
@discord.app_commands.default_permissions(manage_roles=True)
async def forcesave(interaction: discord.Interaction, member: discord.Member):
    await attempt_forcesave(interaction, member)