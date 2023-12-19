import discord
from bot import rolesaver
from events.member_join import restore_member

async def attempt_forcerestore(interaction: discord.Interaction, member: discord.Member):
    try:
        await restore_member(member)
        await interaction.response.send_message(member.name + " has been restored successfully.")
    except Exception as e:
        await interaction.response.send_message("An error has occurred. Please report this to the developer.")
        print(e)

@rolesaver.tree.command(name="forcerestore", description="Restores a user's roles right now, as if they joined the server.")
@discord.app_commands.describe(member="User to restore")
@discord.app_commands.rename(member="user")
async def forcerestore(interaction: discord.Interaction, member: discord.Member):
    await attempt_forcerestore(interaction, member)
