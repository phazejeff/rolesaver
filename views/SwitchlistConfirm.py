from discord import ui, ButtonStyle, Interaction
from bot import rolesaver

class SwitchlistConfirm(ui.View):
    def __init__(self, blacklist):
        self.blacklist = blacklist
        super().__init__()

    @ui.button(label="Confirm", style=ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        rolesaver.database.switch_list(interaction.guild)
        if not self.blacklist.is_blacklist:
            command = await rolesaver.fetch_command_by_name("blacklist", interaction.guild)
            msg = f"Changed to blacklist! Use </blacklist:{command.id}> to add to the blacklist."
        else:
            command = await rolesaver.fetch_command_by_name("whitelist", interaction.guild)
            msg = f"Changed to whitelist! Use </whitelist:{command.id}> to add to the whitelist."

        await interaction.response.edit_message(content=msg, view=None)

        self.stop()
    
    @ui.button(label="Cancel", style=ButtonStyle.grey)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content="Cancelled.", view=None)
        self.stop()
    