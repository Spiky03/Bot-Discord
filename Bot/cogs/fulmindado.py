import discord
from discord.ui import Button, View
from discord.ext import commands
from discord import app_commands
import asyncio

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cogs'))

from buttons import acceptButton, ruleButton, refuseButton, KnucklebonesView

class Knucklebones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
                
    @app_commands.command(name="knucklebones", description="Sfida qualcuno ad una partita a Knucklebones!")
    async def knucklebones(self, ctx: discord.Interaction, p2: discord.User):
        channel_ids = [1196894323606822971]
        if ctx.channel.id not in channel_ids:
            await ctx.response.send_message('_Le parole dei Tavernieri rimbombano:_\n"C\'è un luogo e un momento per ogni cosa! Ma non qui." ', ephemeral=True)
            return
        
        p1 = ctx.user

        embed_sfida = discord.Embed(
            title=f"Sei stato sfidato da {p1.display_name} in una partita di **Knucklebones**!",
            description="### __Accetterai la sfida?__",
            color=discord.Color.yellow()
            )

        # Creazione della view
        view = KnucklebonesView(p1, p2, ctx.channel.id)
        view.add_item(acceptButton())
        view.add_item(refuseButton())
        view.add_item(ruleButton())

        # Invia il messaggio di sfida al giocatore sfidato
        dm_channel = await p2.create_dm()
        view.embed = embed_sfida
        view.message = await dm_channel.send(embed=embed_sfida, view=view)

        # Messaggio di conferma al giocatore sfidante
        await ctx.response.send_message(f"La sfida a Knucklebones è stata inviata a {p2.mention}!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Knucklebones(bot))
