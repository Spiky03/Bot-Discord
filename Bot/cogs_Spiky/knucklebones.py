import discord
from discord.ui import Button, View
from discord.ext import commands
from discord import app_commands
import asyncio

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cogs_Spiky'))

from button_Spiky import acceptButton

class KnucklebonesView(View):
    def __init__(self, p1, p2, channel, timeout=300.0):
        super().__init__(timeout=timeout)
        self.p1 = p1
        self.p2 = p2
        self.channel = channel

    async def on_timeout(self):
        await self.message.edit(content=f"_Mi dispiace {self.p1.mention}, ma la tua proposta di sfida è stata ignorata..._", embed=None, view=None)
        await asyncio.sleep(10)
        await self.message.delete()

class Knucklebones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
                
    @app_commands.command(name="knucklebones", description="Sfida qualcuno ad una partita a Knucklebones!")
    async def knucklebones(self, ctx: discord.Interaction, p2: discord.User):
        channel_id = 1196894323606822971
        if ctx.channel.id != channel_id:
            await ctx.response.send_message('_Le parole dei Tavernieri rimbombano:_\n"C\'è un luogo e un momento per ogni cosa! Ma non qui." ', ephemeral=True)
            return

        p1 = ctx.user
        channel = self.bot.get_channel(channel_id)

        embed_sfida = discord.Embed(title=f"Sei stato sfidato da {p1.display_name} in una partita di **Knucklebones**!", description="### __Accetterai la sfida?__", color=discord.Color.yellow())

        # Creazione della view personalizzata
        view = KnucklebonesView(p1, p2, channel)
        view.add_item(acceptButton())
        
        refuse = Button(label="Rifiuto", style=discord.ButtonStyle.red) # DA RIPORTARE SUI BOTTONI
        async def refuse_callback(ctx: discord.Interaction):
            await ctx.response.send_message("Sfida rifiutata.")
        refuse.callback = refuse_callback
        
        view.add_item(refuse)

        # Invia il messaggio di sfida al giocatore sfidato
        dm_channel = await p2.create_dm()
        view.message = await dm_channel.send(embed=embed_sfida, view=view)

        # Messaggio di conferma al giocatore sfidante
        await ctx.response.send_message(f"La sfida a Knucklebones è stata inviata a {p2.mention}!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Knucklebones(bot))
