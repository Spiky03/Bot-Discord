import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ui import Button, View
                
class Bottone(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="bottone", description="Crea un bottone")
    async def button(self, ctx: discord.Interaction):
        
        # NUMERO DEGLI APPROVATORI
        app = []
        dis = []
        
        # CREA L'EMBED
        embed = discord.Embed(title="Titolo",
                              description=f"Descrizione dell'embed",
                              color=0xFFFF00)
        
        embed.add_field(name="✅ Approvatori",
                        value=">>> Nessuno")
        embed.add_field(name="❌ Disapprovatori",
                        value=">>> Nessuno")

        # CREA I BOTTONI
        buttonApp = Button(label="Approva!", style=discord.ButtonStyle.green, emoji ="✅")
        buttonDis = Button(label="Disapprova!", style=discord.ButtonStyle.grey, emoji ="❌")
        
        # CREA L'INTERAZIONE CON IL BOTTONE E L'AGGIUNGE AL BOTTONE
        async def buttonApp_callback(ctx: discord.Interaction):
            nonlocal app
            nonlocal embed
            # AGGIUNGE IL NOME DELL'APPROVATORE
            if ctx.user.display_name in app:
                app.remove(ctx.user.display_name)
            else:
                app.append(ctx.user.display_name)
            # RIMUOVE IL FIELD PER RIFARLO
            embed.remove_field(0)
            embed.insert_field_at(0, name="✅ Approvatori",
                            value=">>> " + ("\n".join(app) if len(app)!= 0 else "Nessuno"))
            # MODIFICA L'EMBED CON UN FEEDBACK
            await ctx.response.edit_message(embed=embed)
            await ctx.followup.send("Grazie dell'approvazione!", ephemeral=True)
        
        
        async def buttonDis_callback(ctx: discord.Interaction):
            nonlocal dis
            nonlocal embed
            
            if ctx.user.display_name in dis:
                dis.remove(ctx.user.display_name)
            else:
                dis.append(ctx.user.display_name)
            
            embed.remove_field(1)
            embed.insert_field_at(1, name="❌ Disapprovatori",
                               value=">>> " + ("\n".join(dis) if len(dis)!= 0 else "Nessuno"))
            
            await ctx.response.edit_message(embed=embed)
            await ctx.followup.send("Grazie della disapprovazione!", ephemeral=True)
              
        buttonApp.callback = buttonApp_callback
        buttonDis.callback = buttonDis_callback
        
        # CREA IL VIEW AGGIUNGENDOCI IL BOTTONE
        view = View()
        view.add_item(buttonApp) 
        view.add_item(buttonDis)
        
        # INVIA IL MESSAGGIO CON BOTTONI E EMBED ASSIEME
        await ctx.response.send_message(view=view, embed=embed)
        
            
async def setup(bot):
    await bot.add_cog(Bottone(bot))
