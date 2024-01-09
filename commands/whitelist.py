import discord
from typing import Optional
from bot import rolesaver

@rolesaver.tree.command(name="whitelist", description="View current whitelist, or add/remove a role to the whitelist.")
@discord.app_commands.describe(role="Role to add/remove from whitelist. Leave blank to view current whitelist.")
@discord.app_commands.default_permissions(manage_guild=True)
@discord.app_commands.guild_only()
async def whitelist(interaction: discord.Interaction, role: Optional[discord.Role]):
    await interaction.response.defer(thinking=True)
    blacklistdb = rolesaver.database.fetch_blacklist(interaction.guild)
    if blacklistdb.is_blacklist:
        command_switchlist: discord.app_commands.AppCommand = await rolesaver.fetch_command_by_name("switchlist", interaction.guild)
        command_blacklist: discord.app_commands.AppCommand = await rolesaver.fetch_command_by_name("blacklist", interaction.guild)
        await interaction.followup.send(f"You are currently using a blacklist! Use </blacklist:{command_blacklist.id}> instead, or you can </switchlist:{command_switchlist.id}> to switch to a whitelist.")
        return
    

    if role:
        added = rolesaver.database.insert_or_remove_into_blacklist(interaction.guild, role)
        if added:
            await interaction.followup.send(role.name + " has been added to the whitelist.")
        else:
            await interaction.followup.send(role.name + " has been removed from the whitelist.")
        
    else:
        if not blacklistdb or blacklistdb.roles == None or len(blacklistdb.roles) == 0:
            command: discord.app_commands.AppCommand = await rolesaver.fetch_command_by_name("whitelist", interaction.guild)
            cid = command.id

            await interaction.followup.send(f"Whitelist is empty! Use </whitelist:{cid}> and add a role to add to the whitelist.")
        else:
            roles_str = ""
            for r in blacklistdb.roles:
                r = interaction.guild.get_role(r.discord_role_id)
                if r != None: roles_str += r.name + ", "
            roles_str = roles_str[:-2]
            await interaction.followup.send("Whitelisted roles: " + roles_str)