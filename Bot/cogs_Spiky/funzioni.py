# DA AGGIUNGERE I BOTTONI CON LA POSSIBILITà DI EDITARE E CANCELLARE OLTRE ALLE REAZIONI DI APPROVAZIONE

import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import View
import asyncio

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cogs_Spiky'))
    
from button_Spiky import OkButton, EditButton, tipo, num, restr, desc, data 

from datetime import datetime

class Sessione(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="sessione", description="Proponi una tua Sessione ai responsabili Trama & Lore!")
    @app_commands.guild_only()
    async def proposta_sessione(self, ctx: discord.Interaction):
        
        # RUOLO D'APPROVATORE
        role = discord.utils.get(ctx.guild.roles, name="Test")
        
        await ctx.response.defer(thinking=True, ephemeral=True)
    
        if not discord.utils.get(ctx.user.roles, name='Master'):
            await ctx.followup.send('Mi dispiace, ma solo un master può usare questo comando.', ephemeral=True)
            return
        
        dm_channel = await ctx.user.create_dm()
        
        footer = "Inserisci un numero per selezionare una opzione\nPer annullare, digita 'cancella'"
        color = 0xFFFF00
        
        await ctx.followup.send(embed=discord.Embed(title="Proponi una Sessione!",
                                                    description=f"Ti ho inviato un [messaggio diretto](<{ctx.user.dm_channel.jump_url}>) con i passaggi successivi.",
                                                    color=color), ephemeral=True)
        
        self.timeout = 600.0
        self.color = color
        self.footer = footer
        self.dm_channel = dm_channel
    
    # TIPO E DURATA
        session_types = await tipo(self)        
        if session_types == False:
            return
        
    # DESCRIZIONE
        session_desc = await desc(self)
        if session_desc == False:
            return
    # DATA
        session_date, date = await data(self)
        if date == False:
            return
        
    # RESTRIZIONI
        session_res = await restr(self)
        if session_types == False:
                return

    # NUMERO GIOCATORI
        session_amt = await num(self)
        if session_amt == False:
            return
        
    # EMBED FINALE
        embed = discord.Embed(title="",
                            description=f'### Proposta di Sessione di __{ctx.user.mention}__',
                            color=color)
        embed.set_author(name=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
        embed.set_footer(text=str(datetime.today().strftime('%d/%m/%Y %H:%M')))
        
        embed.add_field(name="Tipologia",
                        value=session_types,
                        inline=True)

        embed.add_field(name="Restrizione/i",
                        value=session_res,
                        inline=True)
        
        embed.add_field(name="N° giocatori",
                        value=session_amt,
                        inline=True)
        
        embed.add_field(name="Descrizione della Sessione",
                        value=session_desc[:1024],
                        inline=False)
        
        while len(session_desc) > 1024:
            session_desc = session_desc[1024:]
            embed.add_field(name="",
                            value=session_desc[:1024],
                            inline=False)
        
        if session_date:
            session_date = int(date.timestamp())
            embed.add_field(name="Data",
                            value=f"<t:{session_date}:F>\n:clock2: <t:{session_date}:R>",
                            inline=False)
        else:
            embed.add_field(name="Data",
                            value="Nessuna",
                            inline=False)
        
        embed.add_field(name="✅ Approvatori",
                        value="-",
                        inline=True)
        
        view = View(timeout=None)
        view.add_item(OkButton(label="Approvato"))
        view.add_item(EditButton())
        view.app = []
        view.embed = embed
        view.role = role
        view.color = color
        
        message = await self.bot.get_channel(1213887077511336017).send(embed=embed, view=view)

        # EMBED RISPOSTA
        embedR = discord.Embed(title="La proposta di sessione è stata creata!",
                            description=f"[Clicca qui per visualizzare la proposta](<{message.jump_url}>)",
                            color=color)
        
        await dm_channel.send(embed=embedR)

        

        # THREAD CON BOTTONI
        thread = await message.create_thread(name=f"{sum(1 for i in ctx.channel.threads if ctx.user.name in i.name)+1}° Proposta di {ctx.user.name}")
        await thread.send(content=f"### {ctx.user.mention}, in caso di aggiunte, richieste o dubbi puoi chiedere qui ad un {role.mention}!", silent=True)
        
        self.user = ctx.user
        self.view = view
        self.role = role
        self.thread = thread
        self.approve_task = self.approve.start()
        
    @tasks.loop(seconds = 1)
    async def approve(self):
        try:
            if((len(self.view.app) >= len(self.role.members)//2 )): 
                await self.thread.send(f'### {self.user.mention}, la tua Sessione è stata approvata! ✅\nRicorda di postarla su <#1206935673806782524>.')
                await self.thread.edit(archived=True)
                self.approve_task.cancel()
        
        except asyncio.TimeoutError:
                return
            
async def setup(bot):
    await bot.add_cog(Sessione(bot))