import discord
from typing import Optional
from bot import rolesaver

@rolesaver.tree.command(name="blacklist", description="View current blacklist, or add/remove a role to the blacklist.")
@discord.app_commands.describe(role="Role to add/remove from blacklist. Leave blank to view current blacklist.")
@discord.app_commands.default_permissions(manage_guild=True)
async def blacklist(interaction: discord.Interaction, role: Optional[discord.Role]):
    await interaction.response.defer(thinking=True)
    blacklistdb = rolesaver.database.fetch_blacklist(interaction.guild)
    if not blacklistdb.is_blacklist:
        command_switchlist: discord.app_commands.AppCommand = await rolesaver.fetch_command_by_name("switchlist", interaction.guild)
        command_whitelist: discord.app_commands.AppCommand = await rolesaver.fetch_command_by_name("whitelist", interaction.guild)
        await interaction.followup.send(f"You are currently using a whitelist! Use </whitelist:{command_whitelist.id}> instead, or you can </switchlist:{command_switchlist.id}> to switch to a blacklist.")
        return
    

    if role:
        added = rolesaver.database.insert_or_remove_into_blacklist(interaction.guild, role)
        if added:
            await interaction.followup.send(role.name + " has been added to the blacklist.")
        else:
            await interaction.followup.send(role.name + " has been removed from the blacklist.")
        
    else:
        if not blacklistdb or blacklistdb.roles == None or len(blacklistdb.roles) == 0:
            command: discord.app_commands.AppCommand = await rolesaver.fetch_command_by_name("blacklist", interaction.guild)
            cid = command.id

            await interaction.followup.send(f"Blacklist is empty! Use </blacklist:{cid}> and add a role to add to the blacklist.")
        else:
            roles_str = ""
            for r in blacklistdb.roles:
                r = interaction.guild.get_role(r.discord_role_id)
                if r != None: roles_str += r.name + ", "
            roles_str = roles_str[:-2]
            await interaction.followup.send("Blacklisted roles: " + roles_str)
                