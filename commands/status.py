import discord
from bot import rolesaver

def is_me():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.id == 230119473590304768
    return discord.app_commands.check(predicate)

@rolesaver.tree.command(name="status", description="Change bot status")
@is_me()
async def status(interaction: discord.Interaction, msg: str):
    await interaction.response.defer()
    await rolesaver
    