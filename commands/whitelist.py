import discord
from typing import Optional
from bot import rolesaver

@rolesaver.tree.command(name="whitelist", description="View current whitelist, or add/remove a role to the whitelist.")
@discord.app_commands.describe(role="Role to add/remove from whitelist. Leave blank to view current whitelist.")
async def whitelist(interaction: discord.Interaction, role: Optional[discord.Role]):
    pass