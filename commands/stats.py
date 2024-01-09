import discord
from bot import rolesaver

@rolesaver.tree.command(name="stats", description="Shows the bot's global and server stats")
@discord.app_commands.guild_only()
async def stats(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    log = rolesaver.database.fetch_log(interaction.guild)

    await interaction.followup.send(f"""
## Global Stats
Server Count: **{len(rolesaver.guilds)}**
Members Saved: **{rolesaver.database.nickname_count()}**
Users Saved: **{rolesaver.database.user_count()}**
Unique Roles Saved: **{rolesaver.database.role_count()}**
Shard Count: **{rolesaver.shard_count}**
Latency Average: **{round(rolesaver.latency * 1000)} ms**

## Server Stats
Shard ID: **{interaction.guild.shard_id}**
Shard Latency: **{round(rolesaver.get_shard_latency(interaction.guild.shard_id) * 1000)} ms**
Members Saved: **{rolesaver.database.member_count(interaction.guild)}**
Unique Roles Saved: **{rolesaver.database.guild_role_count(interaction.guild)}**
Logging: **{log.is_logging}**
Logging Channel: **{'<#' + str(log.log_channel) + '>' if log.is_logging else None}**
""")