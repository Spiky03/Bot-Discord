import discord
from discord.ext import commands

class BottoniApprovazione(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        
         
    @discord.ui.button(label='Approva',style=discord.ButtonStyle.green)
    async def button_approve(self,interaction: discord.InteractionMessage,button: discord.ui.Button):
        await interaction.add_reaction('✅')
    @discord.ui.button(label='Disapprova',style=discord.ButtonStyle.red)  
    async def button_disapprove(self,interaction: discord.InteractionMessage,button: discord.ui.Button):
        await interaction.add_reaction('❌')  
        
        
async def setup(bot):
    bot.add_cog(BottoniApprovazione(bot))
    
        