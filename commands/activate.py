import discord
from bot import rolesaver

@rolesaver.tree.command(name="activate", description="Activates Role Saver Premium in this server.")
@discord.app_commands.default_permissions(manage_guild=True)
@discord.app_commands.guild_only()
async def activate(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    if rolesaver.patreon.is_member_premium(interaction.user):
        rolesaver.database.update_patreon_user_guild(interaction.user, interaction.guild)
        await interaction.followup.send(f"Premium is now activated on {interaction.guild.name}! Roles are now being saved.")
    else:
        await interaction.followup.send("You are not an active Patreon. Make sure you have discord connected in your [Patreon account settings](https://www.patreon.com/settings/apps/discord). You can subscribe to premium here: https://www.patreon.com/rolesaver")

