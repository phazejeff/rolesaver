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
            users = self.database.fetch_all_users()
            deleted_count = 0
            roles_cleaned = 0
            
            for user in users:
                if not user.roles:
                    # User has no roles, delete them
                    self.database.delete_user_by_discord_id(user.discord_id)
                    deleted_count += 1
                    continue
                
                # Get all guild IDs for this user's roles
                guild_ids = self.database.get_user_guild_ids(user.discord_id)
                
                # Check if bot is in those guilds and clean up roles for guilds the bot left
                for guild_id in guild_ids:
                    if self.database.is_server_patreon_id(guild_id):
                        continue
                    guild = self.fetch_guild(guild_id)
                    if guild is None:
                        # Bot is not in this guild, remove the user's roles for it
                        self.database.remove_user_roles_for_guild(user.discord_id, guild_id)
                        roles_cleaned += 1
                
                # Check if user still has any roles after cleanup
                remaining_guild_ids = self.database.get_user_guild_ids(user.discord_id)
                if not remaining_guild_ids:
                    # User has no roles left, delete them
                    self.database.delete_user_by_discord_id(user.discord_id)
                    deleted_count += 1
            
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