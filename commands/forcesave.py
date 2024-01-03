import discord
from bot import rolesaver
from events.member_remove import save_member

async def attempt_forcesave(interaction:discord.Interaction, member: discord.Member):
    try:
        await save_member(member)
        await interaction.followup.send(member.name + " has been saved successfully.")
    except Exception as e:
        await interaction.followup.send("An error has occurred. Please report this to the developer.")
        print(e)

@rolesaver.tree.command(name="forcesave", description="Saves a user right now, as if they left the server.")
@discord.app_commands.describe(member="User to save")
@discord.app_commands.rename(member="user")
@discord.app_commands.default_permissions(manage_roles=True)
async def forcesave(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.defer(thinking=True)
    await attempt_forcesave(interaction, member)
