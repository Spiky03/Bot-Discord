# DA AGGIUNGERE I BOTTONI CON LA POSSIBILITà DI EDITARE E CANCELLARE OLTRE ALLE REAZIONI DI APPROVAZIONE

import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio

from datetime import datetime
import dateparser


class Sessione(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="sessione", description="Proponi una tua Sessione ai responsabili Trama & Lore!")
    @app_commands.guild_only()
    async def proposta_sessione(self, ctx: discord.Interaction):
    
        await ctx.response.defer(thinking=True, ephemeral=True)
    
        if not discord.utils.get(ctx.user.roles, name='Master'):
            await ctx.followup.send('Mi dispiace, ma solo un master può usare questo comando.', ephemeral=True)
            return
            
        def check(m):
            return m.author == ctx.user and m.channel == dm_channel
        
        dm_channel = await ctx.user.create_dm()
        
        footer = "Inserisci un numero per selezionare una opzione\nPer annullare, digita 'cancella'"
        color = 0xFFFF00
        
        await ctx.followup.send(embed=discord.Embed(title="Proponi una Sessione!",
                                                    description=f"Ti ho inviato un [messaggio diretto](<{ctx.user.dm_channel.jump_url}>) con i passaggi successivi.",
                                                    color=color), ephemeral=True)
        
        def desc(input_dict):
            output_string = ""
            for key, value in input_dict.items():
                output_string += f"**{key}**. {value}\n"
            return output_string
        
        timeout = 600.0   
    # TIPO
        session_types = {'1':'Vocale', '2': 'Play by Chat', '3': 'Live'}
        embed = discord.Embed(title="Seleziona il tipo di Sessione",
                            description=desc(session_types),
                            color=color)
        embed.set_footer(text=footer)
        await dm_channel.send(embed=embed)
        
        try:
            while True:
                msg = await self.bot.wait_for('message', check=check, timeout=timeout)
                if msg.content.lower() == 'cancella':
                    await ctx.channel.purge(limit=1)
                    await dm_channel.send('Sessione cancellata.')
                    return
                elif msg.content in session_types.keys():
                    session_type = session_types[msg.content]
                    break
                else:
                    await dm_channel.send("Non hai scelto alcuna opzione. Riprova usando una delle opzioni sopra elencate.")
        
        except asyncio.TimeoutError:
            await dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
            return
        
        
    # DURATA
        duration_types = {
        'Vocale': {'1':'One-Shot', '2': 'Bi-Shot', '3': 'Tri-Shot', '4': 'Campagna Breve', '5': 'Campagna Media', '6': 'Campagna Lunga'},
        'Play by Chat': {'1':'Sessione PbC', '2': 'Evento PbC', '3': 'Campagna PbC', '4': 'PbC di Intermezzo'}
        }
        
        try:
            if session_type in duration_types:
                embed = discord.Embed(title="Seleziona la durata della Sessione",
                                    description=desc(duration_types[session_type]),
                                    color=color)
                embed.set_footer(text=footer)
                await dm_channel.send(embed=embed)
        
                while True:
                    msg = await self.bot.wait_for('message', check=check, timeout=timeout)
                    if msg.content.lower() == 'cancella':
                        await dm_channel.send('Sessione cancellata.')
                        return
                    elif msg.content in duration_types[session_type].keys():
                        session_duration = duration_types[session_type][msg.content]
                        break
                    else:
                        await dm_channel.send("Non hai scelto alcuna opzione. Riprova usando una delle opzioni sopra elencate.")
        
                session_types = session_duration if session_type == 'Play by Chat' else session_duration + " " + session_type
        
            else:
                session_types = session_type
        
        except asyncio.TimeoutError:
            await dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
            return

        
        
    # DESCRIZIONE
        try:
            embed = discord.Embed(title="Inserisci la descrizione della Sessione",
                                description="Inserire una descrizione è obbligatorio. Sono consentiti fino a 1600 caratteri.",
                                color=color)
            embed.set_footer(text=footer[-32:])
            await dm_channel.send(embed=embed)
            
            msg = await self.bot.wait_for('message', check=check, timeout=timeout)
            
            if msg.content.lower() == 'cancella':
                await dm_channel.send('Sessione cancellata.')
                return
            else:
                session_desc = msg.content
                
        except asyncio.TimeoutError:
            await dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
            return
        
        
    # DATA
        session_date = True
        embed = discord.Embed(title="Quando inizierà  la Sessione?",
                            description="Digita `None` se non ha una data.\n\n> Venerdì 21.00\n> Domani 18.00\n> Ora\n> Tra 1 ora\n> AAAA-MM-GG 19.00",
                            color=color)
        embed.set_footer(text=footer[-32:])
        await dm_channel.send(embed=embed)
        try:
            while True:
                msg = await self.bot.wait_for('message', check=check, timeout=timeout)
                if msg.content.lower() == 'cancella':
                    await dm_channel.send('Sessione cancellata.')
                    return
                elif msg.content.lower() == 'none':
                    session_date = False
                    break
                else:
                    date = dateparser.parse(msg.content)
                    if date is not None:
                        break
                    else:
                        await dm_channel.send("Non riesco a capire il formato della data. Riprova usando uno dei formati sopra elencati.")
        
        except asyncio.TimeoutError:
            await dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
            return
        
        
    # RESTRIZIONI
        try:
            embed = discord.Embed(title="Inserisci le restrizioni della Sessione",
                                description="Digita `None` se non ha una restrizione.\n\n> Livelli: 5-8\n> Gilda: Diamanti Neri\n> Fazione: Guardie\n> Classe: Bardi\n> Role: Ha visto di persona Gesù",
                                color=color)
            embed.set_footer(text=footer[-32:])
            await dm_channel.send(embed=embed)
            
            msg = await self.bot.wait_for('message', check=check, timeout=timeout)
            if msg.content.lower() == 'none':
                session_res = 'Nessuna'
            elif msg.content.lower() == 'cancella':
                await dm_channel.send('Sessione cancellata.')
                return
            else:
                session_res = msg.content
                
        except asyncio.TimeoutError:
            await dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
            return 
        
        
    # NUMERO GIOCATORI
        try:
            embed = discord.Embed(title="Inserisci un limite di giocatori per la Sessione",
                                description="Utilizza solo numeri. Digita `None` per non mettere un limite.",
                                color=color)
            embed.set_footer(text=footer[-32:])
            await dm_channel.send(embed=embed)
            
            while True:
                msg = await self.bot.wait_for('message', check=check, timeout=timeout)
                if msg.content.lower() == 'cancella':
                    await dm_channel.send('Sessione cancellata.')
                    return
                elif msg.content.lower() == 'none':
                    session_amt = '∞'
                    break
                elif msg.content.isdigit():
                    session_amt = msg.content
                    break
                else:
                    await dm_channel.send("Non hai inserito un numero. Riprova.")
                
        except asyncio.TimeoutError:
            await dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
            return 
        
        
        
    # EMBED FINALE
        embed = discord.Embed(title="",
                            description=f'### Proposta di Sessione di __{ctx.user.mention}__',
                            color=color)
        embed.set_author(name=ctx.user.display_name, icon_url=ctx.user.display_avatar.url)
        embed.set_footer(text=str(datetime.today().strftime('%d/%m/%Y %H:%M')))

        if session_date:
            session_date = int(date.timestamp())
            embed.add_field(name="Data",
                            value=f"<t:{session_date}:f>",
                            inline=False)
        
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
                        value="")
        
        while len(session_desc) > 0:
            if len(session_desc) > 1024:
                embed.add_field(name="",
                                value=session_desc[:1024],
                                inline=False)
                session_desc = session_desc[1024:]
            else:
                embed.add_field(name="",
                                value=session_desc,
                                inline=False)
                session_desc = ""
        
        message = await ctx.channel.send(embed=embed)

        # EMBED RISPOSTA
        embed = discord.Embed(title="La proposta di sessione è stata creata!",
                            description=f"[Clicca qui per visualizzare la proposta](<{message.jump_url}>)",
                            color=color)
        
        await dm_channel.send(embed=embed)

        role = discord.utils.get(ctx.guild.roles, name="Test")

        # THREAD CON REAZIONE
        thread = await message.create_thread(name=f"{sum(1 for i in ctx.channel.threads if ctx.user.name in i.name)+1}° Proposta di {ctx.user.name}")
        await thread.send(content=f"### {ctx.user.mention}, in caso di aggiunte, richieste o dubbi puoi chiedere qui ad un {role.mention}!", silent=True)
        await message.add_reaction('✅')
        await message.add_reaction('❌')

       
        self.checkin_task = self.checkin.start()
        
    @tasks.loop(seconds = 1)
    async def checkin(self, ctx, thread, reaction, role, user):
        if((str(reaction.emoji) == '✅' and reaction.count >= len(role.members)//2 )): 
            await thread.send(f'### {ctx.user.mention}, ti informiamo che la tua Sessione è stata approvata!')
            await thread.edit(archived=True)
            self.checkin_task.cancel()
            
        elif  ((str(reaction.emoji) == '❌' and reaction.count >= len(role.members)//2)):
            await thread.send(f'### {ctx.user.mention}, ti informiamo che la tua Sessione __NON__ è stata approvata.\nPer capirne le motivazioni, contattare un cazzo (anche in questo thread stesso).')
            self.checkin_task.cancel()
              
              
async def setup(bot):
    await bot.add_cog(Sessione(bot))