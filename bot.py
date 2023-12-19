import discord
import os
from database.database import Database

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class RoleSaver(discord.AutoShardedClient):
    def __init__(self):
        super().__init__(intents=intents)
        self.database = Database()
        self.tree = discord.app_commands.CommandTree(self)

    # copies global commands to test server instantly
    async def setup_hook(self):
        GUILD = discord.Object(id=1094848126948491297)
        self.tree.clear_commands(guild=GUILD)
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)
    
    async def on_ready(self):
        print("Logged in as: " + self.user.name)

    async def fetch_command_by_name(self, name: str, guild: discord.Guild) -> discord.app_commands.AppCommand:
        commands = await self.tree.fetch_commands(guild=guild)
        for c in commands:
            if c.name == name:
                return c

    def run(self):
        token = os.environ["DISCORD_TOKEN"]
        super().run(token)

rolesaver = RoleSaver()