import discord
import os
from database.database import Database
from patreon.patreon import Patreon
from discord.ext import tasks

intents = discord.Intents.default()
intents.members = True

class RoleSaver(discord.AutoShardedClient):
    def __init__(self):
        super().__init__(intents=intents, chunk_guilds_at_startup=False)
        self.database = Database()
        self.patreon = Patreon()
        self.tree = discord.app_commands.CommandTree(self)

    # copies global commands to test server instantly
    async def setup_hook(self):
        # GUILD = discord.Object(id=1094848126948491297)
        # self.tree.clear_commands(guild=GUILD)
        # self.tree.copy_global_to(guild=GUILD)
        # await self.tree.sync(guild=GUILD)
        await self.tree.sync()
        self.remove_inactive_patreons.start()
    
    async def on_ready(self):
        print("Logged in as: " + self.user.name)

    async def fetch_command_by_name(self, name: str, guild: discord.Guild) -> discord.app_commands.AppCommand:
        commands = await self.tree.fetch_commands()
        for c in commands:
            if c.name == name:
                return c
            
    def get_shard_latency(self, shard_id: int):
        for i in self.latencies:
            if i[0] == shard_id:
                return i[1]
            else:
                return -1
            
    @tasks.loop(hours=24)
    async def remove_inactive_patreons(self):
        members_in_patreon = rolesaver.patreon.get_premium_members()
        members_in_db = rolesaver.database.get_all_patreon_users()

        for member in members_in_db:
            member: Patreon = member[0]
            if not member.discord_user_id in members_in_patreon:
                rolesaver.database.remove_patreon_user(discord.Object(id=member.discord_user_id))

    def run(self):
        token = os.environ["DISCORD_TOKEN"]
        super().run(token)

rolesaver = RoleSaver()