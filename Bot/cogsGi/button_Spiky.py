import discord
from discord.ui import Button, View
from discord.ext import commands

import dateparser

import asyncio
from datetime import datetime

def check(self, m):
    return m.author == self.user and m.channel == self.dm_channel

def dic(input_dict):
            output_string = ""
            for key, value in input_dict.items():
                output_string += f"**{key}**. {value}\n"
            return output_string
   
async def default(self):
    await self.dm_channel.send("Non hai scelto alcuna opzione. Riprova usando una delle opzioni sopra elencate.")

async def tipo(self):
    session_types = {'1':'Vocale', '2': 'Play by Chat', '3': 'Live'}
    embed = discord.Embed(title="Seleziona il tipo di Sessione",
                        description=dic(session_types),
                        color=self.color)
    embed.set_footer(text=self.footer)
    await self.dm_channel.send(embed=embed)
    
    try:
        while True:
            msg = await self.bot.wait_for('message', check=check(self), timeout=self.timeout)
            if msg.content.lower() == 'cancella':
                await self.dm_channel.send('Sessione cancellata.')
                return False
            elif msg.content in session_types.keys():
                session_type = session_types[msg.content]
                break
            else:
                default
    
    except asyncio.TimeoutError:
        await self.dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
        return False
    
    duration_types = {
        'Vocale': {'1':'One-Shot', '2': 'Bi-Shot', '3': 'Tri-Shot', '4': 'Campagna Breve', '5': 'Campagna Media', '6': 'Campagna Lunga'},
        'Play by Chat': {'1':'Sessione PbC', '2': 'Evento PbC', '3': 'Campagna PbC', '4': 'PbC di Intermezzo'}
        }
        
    try:
        if session_type in duration_types:
            embed = discord.Embed(title="Seleziona la durata della Sessione",
                                description=dic(duration_types[session_type]),
                                color=self.color)
            embed.set_footer(text=self.footer)
            await self.dm_channel.send(embed=embed)
    
            while True:
                msg = await self.bot.wait_for('message', check=check(self), timeout=self.timeout)
                if msg.content.lower() == 'cancella':
                    await self.dm_channel.send('Sessione cancellata.')
                    return False
                elif msg.content in duration_types[session_type].keys():
                    session_duration = duration_types[session_type][msg.content]
                    break
                else:
                    default()
    
            session_types = session_duration if session_type == 'Play by Chat' else session_duration + " " + session_type
    
        else:
            session_types = session_type
            
        return session_type
    
    except asyncio.TimeoutError:
        await self.dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
        return
    
async def desc(self):
    try:
        embed = discord.Embed(title="Inserisci la descrizione della Sessione",
                            description="Inserire una descrizione è obbligatorio. Sono consentiti fino a 1600 caratteri.",
                            color=self.color)
        embed.set_footer(text=self.footer[-32:])
        await self.dm_channel.send(embed=embed)
        
        msg = await self.bot.wait_for('message', check=check(self), timeout=self.timeout)
        
        if msg.content.lower() == 'cancella':
            await self.dm_channel.send('Sessione cancellata.')
            return False
        else:
            return msg.content
            
    except asyncio.TimeoutError:
        await self.dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
        return False
    
async def data(self):
    session_date = True
    embed = discord.Embed(title="Quando inizierà  la Sessione?",
                        description="Digita `None` se non ha una data.\n\n> Venerdì 21.00\n> Domani 18.00\n> Ora\n> Tra 1 ora\n> AAAA-MM-GG 19.00",
                        color=self.color)
    embed.set_footer(text=self.footer[-32:])
    await self.dm_channel.send(embed=embed)
    try:
        while True:
            msg = await self.bot.wait_for('message', check=check(self), timeout=self.timeout)
            if msg.content.lower() == 'cancella':
                await self.dm_channel.send('Sessione cancellata.')
                return False, False
            elif msg.content.lower() == 'none':
                session_date = None
            else:
                date = dateparser.parse(msg.content)
                if date is not None:
                    break
                else:
                    await self.dm_channel.send("Non riesco a capire il formato della data. Riprova usando uno dei formati sopra elencati.")
        return session_date, date
        
    except asyncio.TimeoutError:
        await self.dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
        return False, False
    
async def restr(self):
    try:
        embed = discord.Embed(title="Inserisci le restrizioni della Sessione",
                            description="Digita `None` se non ha una restrizione.\n\n> Livelli: 5-8\n> Gilda: Diamanti Neri\n> Fazione: Guardie\n> Classe: Bardi\n> Role: Ha visto di persona Gesù",
                            color=self.color)
        embed.set_footer(text=self.footer[-32:])
        await self.dm_channel.send(embed=embed)
        
        msg = await self.bot.wait_for('message', check=check(self), timeout=self.timeout)
        if msg.content.lower() == 'none':
            return 'Nessuna'
        elif msg.content.lower() == 'cancella':
            await self.dm_channel.send('Sessione cancellata.')
            return False
        else:
            return msg.content
            
    except asyncio.TimeoutError:
        await self.dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
        return False
    
async def num (self):
    try:
        embed = discord.Embed(title="Inserisci un limite di giocatori per la Sessione",
                            description="Utilizza solo numeri. Digita `None` per non mettere un limite.",
                            color=self.color)
        embed.set_footer(text=self.footer[-32:])
        await self.dm_channel.send(embed=embed)
        
        while True:
            msg = await self.bot.wait_for('message', check=check(self), timeout=self.timeout)
            if msg.content.lower() == 'cancella':
                await self.dm_channel.send('Sessione cancellata.')
                return False
            elif msg.content.lower() == 'none':
                return '∞'
            elif msg.content.isdigit():
                return msg.content
            else:
                await self.dm_channel.send("Non hai inserito un numero. Riprova.")
            
    except asyncio.TimeoutError:
        await self.dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
        return False

def gestisci_caso(numero):
    casi = {1: tipo, 2: restr, 3: num, 4: desc, 5: data}
    return casi.get(numero, default)()   

class EditButton(Button):
        def __init__(self, label="Modifica"):
            super().__init__(label=label, style=discord.ButtonStyle.blurple)
        
        # CREA L'INTERAZIONE FUNZIONE DEL BOTTONE
        async def callback(self, ctx: discord.Interaction):
            view: View = self.view
            color = view.color
            embedOld = view.embed
            embedDict = embedOld.to_dict()
            
            print(embedDict) # DA RIMUOVERE
                
            if embedOld.author.name != ctx.user.display_name:
                await ctx.response.send_message(f"Mi dispiace, ma non sei il creatore di questa proposta", ephemeral=True)
                return
            try:
                while True:
                
                    dm_channel = await ctx.user.create_dm()
                    
                    embed = discord.Embed(title="Che cosa vorresti modificare?",
                                description='',
                                color=color)
                    
                    embed.set_footer(text="Inserisci un numero per selezionare una opzione\nPer annullare, digita 'cancella'")
                    
                    for n, field in enumerate(embedDict['fields'][:-1]):
                        if field['name'] != "":
                            
                            if field['name'] == 'Data' and field['value'] != 'Nessuna':
                                value = datetime.fromtimestamp(int(field['value'][3:13])).strftime('%a %d %b %Y %H:%M') # Cambio formato data
                                translations = {'Mon': 'lun', 'Tue': 'mar', 'Wed': 'mer', 'Thu': 'gio', 'Fri': 'ven', 'Sat': 'sab', 'Sun': 'dom',
                                                'Jan': 'gen', 'Feb': 'feb', 'Mar': 'mar', 'Apr': 'apr', 'May': 'mag', 'Jun': 'giu',
                                                'Jul': 'lug', 'Aug': 'ago', 'Sep': 'set', 'Oct': 'ott', 'Nov': 'nov', 'Dec': 'dic'}

                                for eng, ita in translations.items():
                                    value = value.replace(eng, ita)
                            
                            elif len(field['value']) < 800: # Spezzo descrizioni lunghe
                                value = field['value']
                            
                            else:
                                value = field['value'][:797] + '...'

                            
                            embed.add_field(
                                            name=f"{n+1} - {field['name']}",
                                            value=f"```{value}```",
                                            inline="False" if n not in [0, 1, 2] else "True")
                    
                    await ctx.response.send_message(embed=discord.Embed(title="Modifica la tua Sessione!",
                                                        description=f"Ti ho inviato un [messaggio diretto](<{ctx.user.dm_channel.jump_url}>) con i passaggi successivi.",
                                                        color=color), ephemeral=True)
                    
                    await dm_channel.send(embed=embed)
                    
                    try:
                        while True:
                            msg = await self.bot.wait_for('message', check=check(self), timeout=self.timeout)
                            if msg.content.lower() == 'cancella':
                                await dm_channel.send('Sessione cancellata.')
                                return
                            else:
                                gestisci_caso(msg.content)
                                
                                # MANCA LA MODIFICA COMPLETA
                                
                                embedR = discord.Embed(title="Vorresti continuare a modificare?",
                                                    description="**1** No, ho finito tutto\n**2** Si, continuo a modificare",
                                                    color=color)
                
                                await dm_channel.send(embed=embedR)
                                
                                msg = await self.bot.wait_for('message', check=check(self), timeout=self.timeout)
                                if msg.content == '1':
                                    embedR = discord.Embed(title="L'evento è stato modificato!",
                                                        description=f"[Clicca qui per visualizzare la proposta](<{self.message.jump_url}>)",
                                                        color=color)
                                    
                                    await dm_channel.send(embed=embedR)
                                    return
                                
                                elif msg.content == '2':
                                    break
                    
                    except asyncio.TimeoutError:
                        await dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
                        return
                           
            except asyncio.TimeoutError:
                await dm_channel.send('Sei andato al cesso? Riproveremo più tardi.')
                return  

class OkButton(Button):
        def __init__(self, label, emoji="✅"):
            super().__init__(label=label, style=discord.ButtonStyle.green, emoji=emoji)
        
        # CREA L'INTERAZIONE FUNZIONE DEL BOTTONE
        async def callback(self, ctx: discord.Interaction):
            view: View = self.view
            embed = view.embed
            role = view.role
            app = view.app
            
            if discord.utils.get(ctx.user.roles, name=role.name):
                # AGGIUNGE IL NOME DELL'APPROVATORE
                if ctx.user.display_name in app:
                    app.remove(ctx.user.display_name)
                else:
                    app.append(ctx.user.display_name)
                # RIMUOVE IL FIELD PER RIFARLO
                embed.remove_field(-1)
                embed.add_field(name=f"✅ Approvatori{' (' + str(len(app)) + ')' if len(app) != 0 else ''}",
                                value=(">>> " + "\n".join(app)) if len(app)!= 0 else "-")
                # CHECK APPROVAZIONE
                if len(app) == len(role.members)//2:
                    view=View()
                    embed.set_footer(text="✅ APPROVATA! ✅")                    
                
                # MODIFICA L'EMBED
                await ctx.response.edit_message(embed=embed, view=view)
                    
            else:
                await ctx.response.send_message(f"Mi dispiace, ma non hai il ruolo {role.name}", ephemeral=True)
                    
class NotOkButton(Button):
        def __init__(self, label, emoji="❌"):
            super().__init__(label=label, style=discord.ButtonStyle.grey, emoji=emoji)
        
        
        async def callback(self, ctx: discord.Interaction):
            view: View = self.view
            app = view.app
            dis = view.dis
            embed = view.embed
            role = view.role
                
            if discord.utils.get(ctx.user.roles, name=role.name):
                if ctx.user.display_name in dis:
                    dis.remove(ctx.user.display_name)
                elif ctx.user.display_name in app:
                    app.remove(ctx.user.display_name)
                    dis.append(ctx.user.display_name)
                else:
                    dis.append(ctx.user.display_name)
                
                embed.remove_field(-1)
                embed.add_field(name="❌ Disapprovatori",
                                value=">>> " + ("\n".join(dis) if len(dis)!= 0 else "Nessuno"))
                
                await ctx.response.edit_message(embed=embed)
                    
            else:
                await ctx.response.send_message(f"Mi dispiace, ma non hai il ruolo {role.name}", ephemeral=True)
                
class Buttons(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Buttons(bot))