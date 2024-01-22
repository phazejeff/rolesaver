import discord
from bot import rolesaver

@rolesaver.tree.command(name="premium", description="Info on Premium")
async def premium(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(f"""
__**This is a public bot!**__
That means during periods of high usage, the bot may lose functionality as it hits Discord's rate limit. If you are on a server that needs high reliability, you might want to consider using the Premium bot located here: https://patreon.com/rolesaver
Once the premium instance hits 100 servers, another premium instance will be avaliable to use to avoid bottlenecks. This makes the premium instances far more reliable than the public bot.
"""
    )