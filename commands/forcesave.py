import discord
from bot import rolesaver
from events.member_remove import save_member

async def attempt_forcesave(interaction:discord.Interaction, member: discord.Member):
    try:
        await save_member(member)
        await interaction.response.send_message(member.name + " has been saved successfully.")
    except Exception as e:
        await interaction.response.send_message("An error has occurred. Please report this to the developer.")
        print(e)

@rolesaver.tree.command(name="forcesave", description="Saves a user right now, as if they left the server.")
@discord.app_commands.describe(member="User to save")
@discord.app_commands.rename(member="user")
async def forcesave(interaction: discord.Interaction, member: discord.Member):
    await attempt_forcesave(interaction, member)
