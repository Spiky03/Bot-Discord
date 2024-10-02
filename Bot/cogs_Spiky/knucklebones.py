import discord
from discord.ui import Button, View
from discord.ext import commands
from discord import app_commands
import asyncio

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
        
        p1 = ctx.user
        embed_sfida = discord.Embed(title="Sfida di Knucklebones!", description=f"Sei stato sfidato da {p1.mention} in una partita di **Knucklebones**!\n### __Accetterai la sfida__?", color=discord.Color.yellow())
        
        accept = Button(label="Accetto", style=discord.ButtonStyle.green)
        refuse = Button(label="Rifiuto", style=discord.ButtonStyle.red)
        
        async def accept_callback(self):
            def check(m):
                return m.author == ctx.user and m.channel.id == channel_id
            
            timeout = 600.0
            
            griglia1 = griglia2 = [
                [0,0,0],
                [0,0,0],
                [0,0,0]
            ]
            pt1 = pt2 = 0
            
            async def response():
                nonlocal p1, p2, griglia1, griglia2, pt1, pt2
                embed1 = discord.Embed(color=discord.Color.dark_blue())
                embed1.add_field(name=p1.display_name,
                                value=f"{'👑' if pt1>pt2 else ''} {pt1} Punt{'i' if pt1 != 1 else 'o'}\n" + converti(griglia1,True),
                                inline=False)
                embed2 = discord.Embed(color=discord.Color.dark_red())
                embed2.add_field(name="",
                                value=converti(griglia2,False),
                                inline=False)
                embed2.add_field(name=p2.display_name,
                                value= f"{'👑' if pt2>pt1 else ''} {pt2} Punt{'i' if pt1 != 1 else 'o'}\n",
                                inline=False)
                embed2.set_footer(text="By Spiky03 per Borgo Altrove!")
            
                await self.response.send_message(embeds=[embed1,embed2])
                
            await response()
                
            return
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
        
        async def refuse_callback(self):
            await self.channel.send("Suca 2 volte")
            return
            
        accept.callback = accept_callback
        refuse.callback = refuse_callback
        
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
                

        # Utilizzo della view
        view = MyView(p1, p2, ctx)
        view.add_item(accept)
        view.add_item(refuse)
        
        message = ctx.response.send_message(embed=embed_sfida, view=view, content=p2.mention, silent=True) # DA TOGLIERE IL SILENT
        
        await message
            
async def setup(bot):
    await bot.add_cog(Knucklebones(bot))