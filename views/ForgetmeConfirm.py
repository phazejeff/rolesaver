from discord import ui, ButtonStyle, Interaction
from bot import rolesaver

class ForgetmeConfirm(ui.View):
    def __init__(self, user):
        self.user = user
        super().__init__()

    @ui.button(label="Confirm", style=ButtonStyle.danger)
    async def confirm(self, interaction: Interaction, button: ui.Button):
        rolesaver.database.delete_user(self.user)
        
        await interaction.response.edit_message(content="You have been forgotten. Who are you again?", view=None)

        self.stop()
    
    @ui.button(label="Cancel", style=ButtonStyle.grey)
    async def cancel(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content="Cancelled.", view=None)
        self.stop()