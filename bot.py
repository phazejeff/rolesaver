import discord
import os
from database.database import Database
from events import _on_member_remove, _on_member_join

intents = discord.Intents.default()
intents.members = True

class RoleSaver(discord.AutoShardedClient):
    def __init__(self):
        super().__init__(intents=intents)
        self.database = Database()
    
    async def on_ready(self):
        print("Logged in as: " + self.user.name)

    async def on_member_remove(self, member: discord.Member):
        await _on_member_remove(self.database, member)
    
    async def on_member_join(self, member):
        await _on_member_join(self.database, member)

    def run(self):
        token = os.environ["DISCORD_TOKEN"]
        super().run(token)

rolesaver = RoleSaver()