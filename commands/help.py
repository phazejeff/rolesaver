import discord
from bot import rolesaver

@rolesaver.tree.command(name="help", description="How to use the bot")
async def help(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(f"""
**Thanks for adding Role Saver to your server!**
Remember to put the `Role Saver` role above your other roles, otherwise it cannot access them.

By default, this will save every role a user has. If you want to adjust that, you can use either /blacklist or /whitelist respectively.
                       
If you need any help, you can join the support server and talk to the developer directly: https://discord.gg/gKnRsMaBZ3

__**Keep in mind that this is a public bot!**__
That means during periods of high usage, the bot may lose functionality as it hits Discord's rate limit. If you are on a server that needs high reliability, you might want to consider using the Premium bot located here: https://patreon.com/rolesaver                     
"""
    )