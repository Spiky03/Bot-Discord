from cogsGi.Bottoni import OkButton
import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import Button, View
import asyncio


class prova(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="prova", description="Prova")
    async def prova(self, ctx: discord.Interaction):
        
        embed = discord.Embed(title="Titolo",
                              description=f"Descrizione dell'embed",
                              color=0xFFFF00)
        
        button = OkButton(label="Approva!")
        
        # CREA IL VIEW AGGIUNGENDOCI IL BOTTONE
        view = View(timeout=None)
        view.add_item(button) 
        view.app = []
        view.dis = []
        view.embed = embed
        
        await ctx.response.send_message(view=view, embed=embed)

async def setup(bot):
    await bot.add_cog(prova(bot))