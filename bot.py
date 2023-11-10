import discord
import os

intents = discord.Intents.default()
intents.members = True

class RoleSaver(discord.AutoShardedClient):
    def __init__(self):
        super().__init__(intents=intents)
    
    async def on_ready(self):
        print("Logged in as: " + self.user.name)

    def run(self):
        token = os.environ["DISCORD_TOKEN"]
        super().run(token)