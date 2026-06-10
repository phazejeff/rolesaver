import discord
import os
from database.database import Database
from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True

class RoleSaver(discord.AutoShardedClient):
    def __init__(self):
        super().__init__(intents=intents, chunk_guilds_at_startup=False)
        self.database = Database()
        self.tree = discord.app_commands.CommandTree(self)

    # copies global commands to test server instantly
    async def setup_hook(self):
        # GUILD = discord.Object(id=1094848126948491297)
        # self.tree.clear_commands(guild=GUILD)
        # self.tree.copy_global_to(guild=GUILD)
        # await self.tree.sync(guild=GUILD)
        await self.tree.sync()
        self.cleanup_users_without_guild.start()
    
    async def on_ready(self):
        print("Logged in as: " + self.user.name)

    async def on_shard_ready(self, shard_id: int):
        await self.update_presence()
        print("Logged in as: " + self.user.name + " on shard " + str(shard_id))

    async def on_shard_resumed(self, shard_id: int):
        await self.update_presence()

    @tasks.loop(hours=168)  # 168 hours = 1 week
    async def cleanup_users_without_guild(self):
        """Remove users and their roles if the bot is no longer in their servers"""
        try:
            print("Starting weekly cleanup of users...")
            patreon_guild_ids = self.database.fetch_all_patreon_guild_ids()
            patreon_guild_ids.add(456223064632590344)

            user_guilds = self.database.fetch_all_user_guild_ids()
            all_guild_ids = {guild_id for guild_ids in user_guilds.values() for guild_id in guild_ids}

            fetched_guilds = {}
            for guild_id in all_guild_ids:
                if guild_id in patreon_guild_ids:
                    fetched_guilds[guild_id] = True
                    continue

                guild = self.get_guild(guild_id)
                if guild is not None:
                    fetched_guilds[guild_id] = guild
                    continue

                try:
                    guild = await self.fetch_guild(guild_id)
                    fetched_guilds[guild_id] = guild
                except discord.NotFound:
                    fetched_guilds[guild_id] = None
                except Exception as e:
                    print(f"Warning fetching guild {guild_id}: {e}")
                    fetched_guilds[guild_id] = True

            roles_cleaned = 0
            for discord_id, guild_ids in user_guilds.items():
                stale_guild_ids = {
                    guild_id
                    for guild_id in guild_ids
                    if guild_id not in patreon_guild_ids and fetched_guilds.get(guild_id) is None
                }
                if not stale_guild_ids:
                    continue

                self.database.remove_user_roles_for_guilds(discord_id, stale_guild_ids)
                roles_cleaned += len(stale_guild_ids)

            deleted_count = self.database.delete_users_with_no_roles()
            print(f"Cleanup complete. Deleted {deleted_count} users, cleaned {roles_cleaned} role sets.")
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    @cleanup_users_without_guild.before_loop
    async def before_cleanup(self):
        """Wait until the bot is ready before starting the cleanup task"""
        await self.wait_until_ready()

    async def update_presence(self):
        f = open("status.txt")
        status = f.read()
        f.close()
        game = discord.CustomActivity(status)
        await rolesaver.change_presence(activity=game)

    async def fetch_command_by_name(self, name: str, guild: discord.Guild) -> discord.app_commands.AppCommand:
        commands = await self.tree.fetch_commands()
        for c in commands:
            if c.name == name:
                return c
            
    def get_shard_latency(self, shard_id: int):
        shard = self.get_shard(shard_id)
        return shard.latency

    def run(self):
        token = os.environ["DISCORD_TOKEN"]
        super().run(token)

rolesaver = RoleSaver()