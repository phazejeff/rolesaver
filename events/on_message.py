import discord
from bot import rolesaver

@rolesaver.event
async def on_message(msg: discord.Message):
    print(msg.content)
    if msg.content.startswith("rs.status"):
        status = msg.content[10:]
        if msg.author.id == 230119473590304768:
            f = open("status.txt", "w+")
            f.write(status)
            f.close()
            game = discord.CustomActivity(status)
            await rolesaver.change_presence(activity=game)

            await msg.reply(content="Status changed to: " + status)
        else:
            await msg.reply(content="nah bro. howd you even find this command?")
