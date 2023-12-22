import discord
from typing import Optional
from bot import rolesaver

@rolesaver.tree.command(name="logging", description="Enable/disable logging the saving/restoring of roles in this channel.")
@discord.app_commands.describe(disable="Set to true to disable logging")
@discord.app_commands.default_permissions(manage_guild=True)
async def logging(interaction: discord.Interaction, disable: Optional[bool] = False):
    if disable:
        rolesaver.database.disable_logging(interaction.guild)
        await interaction.response.send_message("Logging disabled.")
    else:
        rolesaver.database.enable_logging(interaction.guild, interaction.channel)
        await interaction.response.send_message(f"<#{interaction.channel.id}> is now the logging channel.")