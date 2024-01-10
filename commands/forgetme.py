import discord
from bot import rolesaver
from views.ForgetmeConfirm import ForgetmeConfirm

@rolesaver.tree.command(name="forgetme", description="Deletes you from the Role Saver database")
async def forgetme(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)

    view = ForgetmeConfirm(interaction.user)
    await interaction.followup.send(content="Are you sure you want to be forgotten? You will not get your roles back on any servers you have left.", view=view, ephemeral=True)
    await view.wait()