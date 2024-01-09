import discord
from typing import Optional
from bot import rolesaver

@rolesaver.tree.command(name="logging", description="Enable/disable logging the saving/restoring of roles in this channel.")
@discord.app_commands.describe(disable="Set to true to disable logging")
@discord.app_commands.default_permissions(manage_guild=True)
@discord.app_commands.guild_only()
async def logging(interaction: discord.Interaction, disable: Optional[bool] = False):
    await interaction.response.defer(thinking=True)
    if disable:
        rolesaver.database.disable_logging(interaction.guild)
        await interaction.followup.send("Logging disabled.")
    else:
        rolesaver.database.enable_logging(interaction.guild, interaction.channel)
        await interaction.followup.send(f"<#{interaction.channel.id}> is now the logging channel.")