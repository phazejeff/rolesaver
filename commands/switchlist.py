import discord
from bot import rolesaver
from views.SwitchlistConfirm import SwitchlistConfirm

@rolesaver.tree.command(description="Switches blacklist to whitelist or vice verse. Will clear current list.")
@discord.app_commands.default_permissions(manage_guild=True)
@discord.app_commands.guild_only()
async def switchlist(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    blacklist = rolesaver.database.fetch_blacklist(interaction.guild)

    msg: str
    if blacklist.is_blacklist:
        msg = "Are you sure you want to change to a whitelist? This will wipe current blacklist data."
    else:
        msg = "Are you sure you want to change to a blacklist? This will wipe current whitelist data."
    
    view = SwitchlistConfirm(blacklist)
    await interaction.followup.send(content=msg, view=view, ephemeral=True)
    await view.wait()
