import discord
from discord.ui import Button, View
from discord.ext import commands
from discord import app_commands
import asyncio
from random import randint as rand

def converti(matrice, p1):
    
    asterischi = [[""] * 3 for _ in range(3)]
    for col in range(3):
        valori_colonna = [matrice[row][col] for row in range(3)]
        for val in set(valori_colonna):
            if val != 0:
                count = valori_colonna.count(val)
                if count == 2:
                    if valori_colonna[1] == val and valori_colonna[2] == val:
                        if not p1:
                            asterischi[1][col] = " * "
                            asterischi[2][col] = "* *"
                        else:
                            asterischi[1][col] = " * "
                            asterischi[2][col] = "* *"
                    elif valori_colonna[0] == val and valori_colonna[1] == val:
                        if not p1:
                            asterischi[0][col] = " * "
                            asterischi[1][col] = "* *"
                        else:
                            asterischi[0][col] = " * "
                            asterischi[1][col] = "* *"
                    else:
                        asterischi[1][col] = "*"
                elif count == 3:
                    if not p1:
                        asterischi[0][col] = "*"
                        asterischi[1][col] = "* *"
                        asterischi[2][col] = "* * *"
                    else:
                        asterischi[2][col] = "*"
                        asterischi[1][col] = "* *"
                        asterischi[0][col] = "* * *"

    # Genera il risultato finale
    risultato = "```\n"
    separatore = "-------------------------\n"
    
    if p1:
        risultato += separatore
        risultato += "|  Sx   |   C   |   Dx  |\n"
        
    for i in range(3):
        risultato += separatore
        if p1:
            risultato += f"|{asterischi[i][0]:^7}|{asterischi[i][1]:^7}|{asterischi[i][2]:^7}|\n"
            risultato += f"|   {matrice[i][0] if matrice[i][0] != 0 else ' '}   |   {matrice[i][1] if matrice[i][1] != 0 else ' '}   |   {matrice[i][2] if matrice[i][2] != 0 else ' '}   |\n"
            risultato += "|       |       |       |\n"
        else:
            risultato += "|       |       |       |\n"
            risultato += f"|   {matrice[i][0] if matrice[i][0] != 0 else ' '}   |   {matrice[i][1] if matrice[i][1] != 0 else ' '}   |   {matrice[i][2] if matrice[i][2] != 0 else ' '}   |\n"
            risultato += f"|{asterischi[i][0]:^7}|{asterischi[i][1]:^7}|{asterischi[i][2]:^7}|\n"

    risultato += separatore
    if not p1:
        risultato += "|  Sx   |   C   |   Dx  |\n"
        risultato += separatore

    return risultato + "\n```"

class Knucklebones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
                
    @app_commands.command(name="knucklebones", description="Sfida qualcuno ad una partita a Knucklebones!")
    async def knucklebones(self, ctx: discord.Interaction, p2: discord.User):
        channel_id = 1208063577496223825
        if ctx.channel.id != channel_id:
            await ctx.response.send_message('_Le parole dei Tavernieri rimbombano:_\n"C\'è un luogo e un momento per ogni cosa! Ma non qui." ', ephemeral=True)
            return

    class MyView(View):
            def __init__(self, p1, p2, ctx):
                super().__init__(timeout=300)
                self.p1 = p1
                self.p2 = p2
                self.ctx = ctx
            
            async def on_timeout(self):
                await self.ctx.edit_original_response(content=f"_Mi dispiace {self.p1.mention}, ma la tua proposta di sfida è stata ignorata..._", embed=None, view=None)
                await asyncio.sleep(10)
                await self.ctx.delete_original_response()
                
    class MyButton(Button):
        def __init__(self):
            super().__init_()
        p1 = ctx.user
        embed_sfida = discord.Embed(title=f"Sei stato sfidato da {p1.display_name} in una partita di **Knucklebones**!", description="### __Accetterai la sfida?__", color=discord.Color.yellow())

        accept = Button(label="Accetto", style=discord.ButtonStyle.green)
        refuse = Button(label="Rifiuto", style=discord.ButtonStyle.red)
        tira = Button(label="Tira", style=discord.ButtonStyle.blurple)
        resa = Button(label="Resa", style=discord.ButtonStyle.gray)
 
        async def accept_callback(ctx: discord.Interaction):
            channel = self.bot.get_channel(channel_id)

            if channel is None:
                await ctx.response.send_message("Canale non trovato.", ephemeral=True)
                return

            timeout = 20.0

            griglia1 = griglia2 = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]

            pt1 = pt2 = 0

            def griglie():
                nonlocal p1, p2, griglia1, griglia2, pt1, pt2
                embed1 = discord.Embed(color=discord.Color.dark_blue())
                embed1.add_field(name=p1.display_name,
                                 value=f"{'👑' if pt1 > pt2 else ''} {pt1} Punt{'i' if pt1 != 1 else 'o'}\n" + converti(griglia1, True),
                                 inline=False)
                embed2 = discord.Embed(color=discord.Color.dark_red())
                embed2.add_field(name="",
                                 value=converti(griglia2, False),
                                 inline=False)
                embed2.add_field(name=p2.display_name,
                                 value=f"{'👑' if pt2 > pt1 else ''} {pt2} Punt{'i' if pt1 != 1 else 'o'}\n",
                                 inline=False)
                embed2.set_footer(text="By Spiky03 per Borgo Altrove!")

                return [embed1, embed2]

            view=MyView(p1, p2, ctx)
            view.add_item(resa)
            view.add_item(tira)
            
            msg = await channel.send(embeds=griglie())
            
            embed = discord.Embed(title="Hai accettato la sfida a **Knucklebones**", description=f"[Vai alla sfida!](<{msg.jump_url}>)")
            await ctx.response.send_message(embed=embed, ephemeral=True)

            # Inizio dei giochi
            embed = discord.Embed(title=f"{p2.display_name} è tuo turno!", 
                                  description="Scegli cosa fare!",
                                  color=discord.Color.dark_red())
            embed.set_author(name=p2.display_name,
                             icon_url=p2.avatar)
            msg = await channel.send(embed=embed, view=view)

        async def tira_callback(ctx: discord.Interaction):
            
            pass
            
            
        
        async def resa_callback(ctx: discord.Interaction):
            pass
        
        async def refuse_callback(ctx: discord.Interaction):
            await ctx.response.send_message("Suca")
            
        accept.callback = accept_callback
        refuse.callback = refuse_callback
        tira.callback = tira_callback
        resa.callback = resa_callback

        # Utilizzo della view
        view = MyView(p1, p2, ctx)
        view.add_item(accept)
        view.add_item(refuse)

        dm_channel = await p2.create_dm()

        await dm_channel.send(embed=embed_sfida, view=view)
        await ctx.response.send_message(f"La sfida a Knucklebones è stata inviata a {p2.mention}!", ephemeral=True)        
            
async def setup(bot):
    await bot.add_cog(Knucklebones(bot))