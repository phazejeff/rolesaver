import discord
import os
from database.database import Database

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
    
    async def on_ready(self):
        print("Logged in as: " + self.user.name)

    async def on_shard_ready(self, shard_id: int):
        await self.update_presence()
        print("Logged in as: " + self.user.name + " on shard " + str(shard_id))

    async def on_shard_resumed(self, shard_id: int):
        await self.update_presence()

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