import discord
from discord.ui import Button, View
<<<<<<< HEAD
from discord.ext import commands

=======
                   
>>>>>>> 64f8d285d7758592df0085b2711cdf4f0e67d9af
class OkButton(Button):
        def __init__(self, label, emoji="✅"):
            super().__init__(label=label, style=discord.ButtonStyle.blurple, emoji=emoji)
        
        # CREA L'INTERAZIONE FUNZIONE DEL BOTTONE
        async def callback(self, ctx: discord.Interaction):
            view: View = self.view
            app = view.app
            dis = view.dis
            embed = view.embed
            role = view.role
                
            if discord.utils.get(ctx.user.roles, name=role.name):
                # AGGIUNGE IL NOME DELL'APPROVATORE
                if ctx.user.display_name in app:
                    app.remove(ctx.user.display_name)
                else:
                    app.append(ctx.user.display_name)
                # RIMUOVE IL FIELD PER RIFARLO
                embed.remove_field(-1)
                embed.add_field(name="✅ Approvatori",
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