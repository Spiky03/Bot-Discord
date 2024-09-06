import discord
from discord.ui import Button, View
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
import dateparser

class EditButton(Button):
        def __init__(self, bot, label="Modifica",):
            super().__init__(label=label, style=discord.ButtonStyle.blurple)
            self.bot = bot
        # CREA L'INTERAZIONE FUNZIONE DEL BOTTONE
        async def callback(self, ctx: discord.Interaction):
            view: View = self.view
            color = view.color
            embed = view.embed
            embedDict = embed.to_dict()
            timeout = 3600.0  
            fields = embedDict['fields']
            print(embedDict) #DA RIMUOVERE
                
            if embed.author.name == ctx.user.display_name:
                
                def check(m):
                    return m.author == ctx.user and m.channel == dm_channel
        
                dm_channel = await ctx.user.create_dm()
                
                embed = discord.Embed(title="Che cosa vorresti modificare?",
                            description='',
                            color=color)
                
                embed.set_footer(text="Inserisci un numero per selezionare una opzione\nPer annullare, digita 'cancel'")
                
                for n, field in enumerate(embedDict['fields'][:-1]):
                    if field['name'] != "":
                        
                        if field['name'] == 'Data':
                            value = datetime.fromtimestamp(int(field['value'][3:-3])).strftime('%a %d %b %Y %H:%M') # Cambio formato data
                            translations = {
                                            'Mon': 'lun', 'Tue': 'mar', 'Wed': 'mer', 'Thu': 'gio', 'Fri': 'ven', 'Sat': 'sab', 'Sun': 'dom',
                                            'Jan': 'gen', 'Feb': 'feb', 'Mar': 'mar', 'Apr': 'apr', 'May': 'mag', 'Jun': 'giu',
                                            'Jul': 'lug', 'Aug': 'ago', 'Sep': 'set', 'Oct': 'ott', 'Nov': 'nov', 'Dec': 'dic'
                                            }

                            for eng, ita in translations.items():
                                value = value.replace(eng, ita)
                        
                        elif len(field['value']) < 800: # Spezzo descrizioni lunghe
                            value = field['value']
                        
                        else:
                            value = field['value'][:797] + '...'

                        
                        embed.add_field(
                                        name=f"{n+1} - {field['name']}",
                                        value=f"```{value}```",
                                        inline="False" if n in [0, 4] else "True")
                
                await ctx.response.send_message(embed=discord.Embed(title="Modifica la tua Sessione!",
                                                    description=f"Ti ho inviato un [messaggio diretto](<{ctx.user.dm_channel.jump_url}>) con i passaggi successivi.",
                                                    color=color), ephemeral=True)
                
                await dm_channel.send(embed=embed)
                print(fields)
                session_types = {'1':'Vocale', '2': 'Play by Chat', '3': 'Live'}
                duration_types = {
                'Vocale': {'1':'One-Shot', '2': 'Bi-Shot', '3': 'Tri-Shot', '4': 'Campagna Breve', '5': 'Campagna Media', '6': 'Campagna Lunga'},
                'Play by Chat': {'1':'Sessione PbC', '2': 'Evento PbC', '3': 'Campagna PbC', '4': 'PbC di Intermezzo'}
                 }
                while True:
                        try:
                            msg = await self.bot.wait_for('message', check=check, timeout=timeout)
                            if msg.content.lower() == "cancella":
                                break
                            elif msg.content in field['name']:
                                fields = msg.content
                                if fields == "Tipologia":
                                    await ctx.user.send("Scegli la tipologia:\n"
                                                        "1. Vocale\n"
                                                        "2. Play by Chat\n"
                                                        "3. Live")
                                    msg = await self.bot.wait_for('message', check=check, timeout=timeout)
                                    if msg.content in session_types:
                                        session_type = session_types[msg.content]
                                        await ctx.user.send(f"Scegli la durata per {session_type}:\n" +
                                                            "\n".join([f"{k}. {v}" for k, v in duration_types[session_type].items()]))
                                        msg = await self.bot.wait_for('message', check=check, timeout=timeout)
                                        if msg.content in duration_types[session_type]:
                                            duration_type = duration_types[session_type][msg.content]
                                            view.embed[fields] = f"{session_type} - {duration_type}"
                                            await ctx.user.send(f"Tipologia aggiornata a: {session_type} - {duration_type}")
                                        else:
                                            await ctx.user.send("Durata non valida. Riprova.")
                                    else:
                                        await ctx.user.send("Tipologia non valida. Riprova.")
                                else:
                                    await ctx.user.send(f"Inserisci il nuovo valore per {fields}:")
                                    value = await self.bot.wait_for('message', check=check, timeout=timeout)
                                    view.emebed[fields] = value.content
                                    await ctx.user.send(f"{fields} aggiornato a: {value.content}\n"
                                                        "Digita il numero del prossimo campo da modificare o 'cancella' per terminare.")
                            else:
                                await ctx.user.send("Numero non valido. Riprova.")
                        except asyncio.TimeoutError:
                            await ctx.user.send("Tempo scaduto. Sessione annullata.")
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
                embed.add_field(name=f"✅ Approvatori ({len(app)})",
                                value=">>> " + ("\n".join(app) if len(app)!= 0 else "Nessuno"))
                # MODIFICA L'EMBED
                await ctx.response.edit_message(embed=embed)
                    
            else:
                await ctx.response.send_message(f"Mi dispiace, ma non hai il ruolo {role.name}", ephemeral=True)
            
            
            @tasks.loop(seconds = 1)
            async def check(self, ctx, thread, role, reaction, view, user):
                
                try:
                    print(len(view.app))
                    if((len(view.app) >= len(role.members)//2 )): 
                        await thread.send(f'### {ctx.user.mention}, ti informiamo che la tua Sessione è stata approvata!')
                        await thread.edit(archived=True)
                        self.check_task.cancel()
                    
                
                except asyncio.TimeoutError:
                        return   
                    
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