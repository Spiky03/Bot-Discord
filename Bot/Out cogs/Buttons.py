import discord
from discord.ui import Button, View
from discord.ext import commands

from datetime import datetime
import dateparser

class EditButton(Button):
        def __init__(self, label="Modifica"):
            super().__init__(label=label, style=discord.ButtonStyle.blurple)
        
        # CREA L'INTERAZIONE FUNZIONE DEL BOTTONE
        async def callback(self, ctx: discord.Interaction):
            view: View = self.view
            color = view.color
            embed = view.embed
            embedDict = embed.to_dict()
            
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
                                        inline="False" if n in [0, 4] else "True")
                
                await ctx.response.send_message(embed=discord.Embed(title="Modifica la tua Sessione!",
                                                    description=f"Ti ho inviato un [messaggio diretto](<{ctx.user.dm_channel.jump_url}>) con i passaggi successivi.",
                                                    color=color), ephemeral=True)
                
                await dm_channel.send(embed=embed)

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