import discord
from bot import rolesaver

@rolesaver.tree.command(name="help", description="How to use the bot")
async def help(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(f"""
**Thanks for adding Role Saver Premium to your server!**
In order to activate, just use /activate in the server you want the bot activated in. You can only have 1 server activated per Discord account

Remember to put the `Role Saver Premium` role above your other roles, otherwise it cannot access them.

By default, this will save every role a user has. If you want to adjust that, you can use either /blacklist or /whitelist respectively.
                       
If you need any help, you can join the support server and talk to the developer directly: https://discord.gg/gKnRsMaBZ3                   
"""
    )