import discord
from discord.ui import Button, View
from discord.ext import commands
import asyncio

from random import randint

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

def converti(matrice, p1):
    asterischi = [[""] * 3 for _ in range(3)]
    for col in range(3):
        valori_colonna = [matrice[row][col] for row in range(3)]
        for val in set(valori_colonna):
            if val != 0:
                count = valori_colonna.count(val)
                if count == 2:
                    if valori_colonna[0] == val and valori_colonna[2] == val:  # Righe diverse da quella centrale
                        if not p1:
                            asterischi[0][col] = " * "
                            asterischi[2][col] = "* *"
                        else:
                            asterischi[0][col] = "* *"
                            asterischi[2][col] = " * "
                    elif valori_colonna[1] == val and valori_colonna[2] == val:
                        if not p1:
                            asterischi[1][col] = " * "
                            asterischi[2][col] = "* *"
                        else:
                            asterischi[1][col] = "* *"
                            asterischi[2][col] = " * "
                    elif valori_colonna[0] == val and valori_colonna[1] == val:
                        if not p1:
                            asterischi[0][col] = " * "
                            asterischi[1][col] = "* *"
                        else:
                            asterischi[0][col] = "* *"
                            asterischi[1][col] = " * "
                    else:
                        asterischi[1][col] = "*"
                elif count == 3:
                    if not p1:
                        asterischi[0][col] = "*"
                        asterischi[1][col] = "* *"
                        asterischi[2][col] = "* * *"
                    else:
                        asterischi[0][col] = "* * *"
                        asterischi[1][col] = "* *"
                        asterischi[2][col] = "*"

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

def griglie(p1, p2, griglia1, griglia2, pt1, pt2):
            embed1 = discord.Embed(color=discord.Color.dark_blue())
            embed1.add_field(name=p1.display_name,
                             value=f"{'👑' if pt1 > pt2 else ''} {pt1} Punt{'i' if pt1 != 1 else 'o'}\n" + converti(griglia1, True),
                             inline=False)
            embed2 = discord.Embed(color=discord.Color.dark_red())
            embed2.add_field(name="",
                             value=converti(griglia2, False),
                             inline=False)
            embed2.add_field(name=p2.display_name,
                             value=f"{'👑' if pt2 > pt1 else ''} {pt2} Punt{'i' if pt2 != 1 else 'o'}\n",
                             inline=False)
            embed2.set_footer(text="By Spiky03 per Borgo Altrove!")

            return [embed1, embed2]
        
def pt(griglie):
    punteggi = []
    for griglia in griglie:
        punteggio = 0
        for c in range(3):
            col_vals = [griglia[r][c] for r in range(3)]
            for val in set(col_vals):
                if val != 0:
                    count = col_vals.count(val)
                    if count == 1:
                        punteggio += val
                    elif count == 2:
                        punteggio += val * 4
                    elif count == 3:
                        punteggio += val * 9
        punteggi.append(punteggio)
    return punteggi
        
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

class resaButton(Button):
    def __init__(self):
        super().__init__(label="Resa", style=discord.ButtonStyle.grey)
        
    async def callback(self, ctx: discord.Interaction):
        view: fulmidadoView = self.view
        winner = view.p1 if view.turn == "p2" else view.p2
        loser = view.p2 if view.turn == "p2" else view.p1
        color = discord.Color.dark_blue() if winner == view.p1 else discord.Color.dark_red()

        # Aggiorna gli embed delle griglie con il colore del vincitore
        griglia1_embed = discord.Embed(color=color)
        griglia1_embed.add_field(name=view.p1.display_name,
                                 value=f"{'👑' if winner == view.p1 else ''} {view.pt1} Punt{'i' if view.pt1 != 1 else 'o'}\n" + converti(view.griglia1, True),
                                 inline=False)

        griglia2_embed = discord.Embed(color=color)
        griglia2_embed.add_field(name="",
                                 value=converti(view.griglia2, False),
                                 inline=False)
        griglia2_embed.add_field(name=view.p2.display_name,
                                 value=f"{'👑' if winner == view.p2 else ''} {view.pt2} Punt{'i' if view.pt2 != 1 else 'o'}\n",
                                 inline=False)
        griglia2_embed.set_footer(text="By Spiky03 per Borgo Altrove!")

        # Crea l'embed per dichiarare il vincitore
        embed = discord.Embed(
            title=f"{loser.display_name} si è arreso!",
            description=f"Il vincitore è __{winner.mention}__!",
            color=discord.Color.green()
        )

        # Modifica il messaggio originale con gli embed aggiornati
        await ctx.response.edit_message(embeds=[griglia1_embed, griglia2_embed, embed], view=None)

class acceptButton(Button):
    def __init__(self):
        super().__init__(label="Accetto", style=discord.ButtonStyle.green)
            
    async def callback(self, ctx: discord.Interaction):
        view: fulmidadoView = self.view
        channel = view.channel
        view.stop()
        
        view = fulmidadoView(view.p1, view.p2, channel)
        view.add_item(tiraButton("p2"))

        embed = discord.Embed(
            title=f"{view.p2.display_name} è il tuo turno!", 
            description="Scegli cosa fare!",
            color=discord.Color.dark_red()
        )
        embed.set_author(
            name=view.p2.display_name,
            icon_url=view.p2.avatar.url
        )
        
        view.message = await channel.send(embeds=griglie(view.p1, view.p2, view.griglia1, view.griglia2, view.pt1, view.pt2) + [embed], view=view)

        embed = discord.Embed(
            title=f"Hai accettato la sfida a **Fulmidado** contro {view.p1.display_name}",
            description=f"[Vai alla sfida!](<{view.message.jump_url}>)",
            color=discord.Color.green()
            )
        await ctx.message.edit(embed=embed, view=None)

class refuseButton(Button):
    def __init__(self):
        super().__init__(label="Rifiuto", style=discord.ButtonStyle.red)
        
    async def callback(self, ctx: discord.Interaction):
        # Invia un messaggio di conferma
        view: fulmidadoView = self.view
        embed = view.embed
        embed.description, embed.color = "La proposta è stata rifiutata.", discord.Color.red()
        # Aggiorna il messaggio originale per rimuovere i pulsanti
        await ctx.response.edit_message(embed=embed, view=None)
        dm_channel1 = await view.p1.create_dm()
        await dm_channel1.send(content=f"_Mi dispiace, la tua sfida a **Fulmidado** verso {view.p2.mention} è stata rifiutata._")
        view.stop()

class tiraButton(Button):
    def __init__(self, p):
        super().__init__(label="Tira!", style=discord.ButtonStyle.blurple)
        self.p = p
        self.emojis = {
            1:"<:d6_1:1292657675221340190>",
            2:"<:d6_2:1292657681311731762>",
            3:"<:d6_3:1292657676366647347>",
            4:"<:d6_4:1292657677561757726>", 
            5:"<:d6_5:1292657678933426217>",
            6:"<:d6_6:1292657680044785736>", 
        }
    async def callback(self, ctx: discord.Interaction):
        view: fulmidadoView = self.view
        player, griglia = (view.p2, view.griglia2) if self.p == "p2" else (view.p1, view.griglia1)

        # EMBED Colonna
        rolled_number = randint(1, 6)
        embed = discord.Embed(
            title=f"{player.display_name} ha tirato un {self.emojis[rolled_number]}!",
            description=f"Scegli in quale colonna inserire il **{rolled_number}**.",
            color=discord.Color.dark_blue() if self.p == "p1" else discord.Color.dark_red()
        )
        embed.set_author(
            name=player.display_name,
            icon_url=player.avatar.url
        )

        # Aggiunta dei bottoni per la scelta della colonna
        view.clear_items()
        # Verifica se la colonna "Sx" è piena
        if any(cell == 0 for cell in [row[0] for row in griglia]):
            view.add_item(ColumnButton("Sx", rolled_number, self.p))
        # Verifica se la colonna "C" è piena
        if any(cell == 0 for cell in [row[1] for row in griglia]):
            view.add_item(ColumnButton("C", rolled_number, self.p))
        # Verifica se la colonna "Dx" è piena
        if any(cell == 0 for cell in [row[2] for row in griglia]):
            view.add_item(ColumnButton("Dx", rolled_number, self.p))
        view.add_item(resaButton())

        await ctx.response.edit_message(embeds=griglie(view.p1, view.p2, view.griglia1, view.griglia2, view.pt1, view.pt2) + [embed], view=view)

class ColumnButton(Button):
    def __init__(self, label, rolled_number, p):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.rolled_number = rolled_number
        self.p = p
        
    async def callback(self, ctx: discord.Interaction):
        view: fulmidadoView = self.view
        # Logica per inserire il valore nella griglia
        col = {"Sx": 0, "C": 1, "Dx": 2}[self.label]

        def complete(matrice):
            for row in matrice:
                for num in row:
                    if num == 0:
                        return False
            return True
        
        # Trova la prima cella vuota nella colonna partendo dall'alto per p2 e dal basso per p1
        if self.p == "p2":
            player, next_player = view.p2, view.p1
            for row in view.griglia2:
                if row[col] == 0:
                    row[col] = self.rolled_number
                    break

            # Rimuove i numeri uguali dalla colonna dell'avversario e fa scalare i numeri
            for i in range(3):
                if view.griglia1[i][col] == self.rolled_number:
                    view.griglia1[i][col] = 0

            # Scala i numeri dall'alto verso il basso per p1
            for i in range(2, 0, -1):
                if view.griglia1[i][col] == 0:
                    # Trova la prima cella sopra non vuota
                    for j in range(i - 1, -1, -1):
                        if view.griglia1[j][col] != 0:
                            view.griglia1[i][col], view.griglia1[j][col] = view.griglia1[j][col], 0
                            break
                            
            end = complete(view.griglia2)

        else:
            player, next_player = view.p1, view.p2
            for i in range(2, -1, -1):
                if view.griglia1[i][col] == 0:
                    view.griglia1[i][col] = self.rolled_number
                    break

            # Rimuove i numeri uguali dalla colonna dell'avversario e fa scalare i numeri
            for i in range(3):
                if view.griglia2[i][col] == self.rolled_number:
                    view.griglia2[i][col] = 0

            # Scala i numeri dal basso verso l'alto per p2
            for i in range(2):
                if view.griglia2[i][col] == 0:
                    # Trova la prima cella sopra non vuota
                    for j in range(2, i, -1):
                        if view.griglia2[j][col] != 0:
                            view.griglia2[i][col], view.griglia2[j][col] = view.griglia2[j][col], 0
                            break
            
            end = complete(view.griglia1)

        # Aggiorna i punteggi
        view.pt1, view.pt2 = pt([view.griglia1, view.griglia2])

        if end:
            winner = view.p1 if view.pt1 > view.pt2 else view.p2
        
            # Aggiorna l'embed per mostrare il vincitore
            embed = discord.Embed(
            title=f"{player.display_name} ha completato la sua griglia!",
            description=f"Il vincitore è __{winner.mention}__!",
            color=discord.Color.green()
            )
            embeds = griglie(view.p1, view.p2, view.griglia1, view.griglia2, view.pt1, view.pt2) + [embed]
            if view.pt1 > view.pt2:
                embeds[1].color = discord.Color.dark_blue()
            else:
                embeds[0].color = discord.Color.dark_red()
            view.stop()
            await ctx.response.edit_message(embeds=embeds, view=None)

            
        else:
            # Aggiorna il turno al prossimo giocatore
            view.turn = "p1" if view.turn == "p2" else "p2"
            
            # Ripristina i bottoni per il prossimo giocatore
            view.clear_items()
            view.add_item(tiraButton(view.turn))
            view.add_item(resaButton())
            
            # Aggiorna l'embed per mostrare la nuova situazione del gioco
            embed = discord.Embed(
                title=f"{next_player.display_name} è il tuo turno!",
                description="Scegli cosa fare!",
                color=discord.Color.dark_blue() if view.turn == "p1" else discord.Color.dark_red()
            )
            embed.set_author(
                name=next_player.display_name,
                icon_url=next_player.avatar.url
            )
            await ctx.response.edit_message(embeds=griglie(view.p1, view.p2, view.griglia1, view.griglia2, view.pt1, view.pt2) + [embed], view=view)

class ruleButton(Button):
    def __init__(self):
        super().__init__(label="Regolamento", style=discord.ButtonStyle.blurple)
        
    async def callback(self, ctx: discord.Interaction):
        # Crea un embed per il regolamento
        embed = discord.Embed(
            title="Regolamento di Fulmidado",
            description="Regole ufficiali per il torneo di Fulmidado durante Borgofest",
            color=discord.Color.blue()
        )

        # Aggiunge le sezioni al regolamento
        embed.add_field(
            name="Obiettivo del gioco",
            value="Ottenere il punteggio più alto nelle griglie rispetto all'avversario.",
            inline=False
        )
        
        embed.add_field(
            name="Come giocare",
            value=(
                "Ogni giocatore tira un __d6__ e sceglie una colonna dove inserire il numero ottenuto.\n"
                "Il valore del dado viene moltiplicato in base a quante volte lo stesso numero compare in una colonna:\n"
                "- 1 volta: x1\n"
                "- 2 volte: x4\n"
                "- 3 volte: x9"
            ),
            inline=False
        )

        embed.add_field(
            name="Rimuovi numeri dell'avversario",
            value="Se posizioni un numero che coincide con uno o più numeri nella stessa colonna dell'avversario, questi vengono rimossi.",
            inline=False
        )
        
        embed.add_field(
            name="Vittoria",
            value="Vince chi ha il punteggio più alto quando uno dei due giocatori completa la griglia.",
            inline=False
        )
        
        # Modalità di gioco Borgofest
        embed.add_field(
            name="Punti Borgofest",
            value=(
                "Durante Borgofest, oltre ai normali punti, i giocatori accumulano **Punti Borgofest** a seconda della modalità scelta, sottraendoli all'avversario in caso di vincita.\n La modalità va scelta assieme all'avversario prima di chiedere la sfida, e queste sono:"
            ),
            inline=False
        )

        embed.add_field(
            name="Modalità di gioco",
            value=(
                "1. **Mezzo**: Il vincente sottrae metà della differenza di punti al perdente.\n"
                "2. **Intero**: Il vincente sottrae la differenza di punti al perdente.\n"
                "3. **Doppio**: Il vincente sottrae il doppio della differenza di punti al perdente."
            ),
            inline=False
        )

        # Invia il regolamento come embed all'utente che ha cliccato il pulsante
        await ctx.response.send_message(embed=embed, ephemeral=True)

class fulmidadoView(View):
    def __init__(self, p1, p2, channel, timeout=3600.0):
        super().__init__(timeout=timeout)
        self.p1 = p1
        self.p2 = p2
        self.channel = channel
        self.pt1 = 0
        self.pt2 = 0
        self.griglia1 = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.griglia2 = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.turn = "p2"  # Inizia p2 (l'avversario)
        self.message = None  # Messaggio originale da aggiornare in caso di timeout

    async def on_timeout(self):
        if self.message:
            dm_channel1 = await self.p1.create_dm()
            dm_channel2 = await self.p2.create_dm()
            if len(self.message.embeds) < 3:
                self.message.embeds[0].description = "La proposta è stata rifiutata in automatico per inattività."
                self.message.embeds[0].color = discord.Color.red()
                await self.message.edit(embeds=[self.message.embeds[0]], view=None)
                await dm_channel2.send(content=f"_Mi dispiace, la tua sfida a **Fulmidado** verso {self.p2.mention} è stata annullata a causa dell'inattività._")
            else:  
                await dm_channel1.send(content="_Mi dispiace, la partita è scaduta e ritenuta invalida a causa dell'inattività._", embeds=self.message.embeds[:2])
                await dm_channel2.send(content="_Mi dispiace, la partita è scaduta e ritenuta invalida a causa dell'inattività._", embeds=self.message.embeds[:2])
                await self.message.delete()
                         
    async def interaction_check(self, interaction: discord.Interaction):
        # Permetti solo all'autore del comando di interagire con la view
        player = self.p2 if self.turn == "p2" else self.p1
        
        if interaction.user != player:
            await interaction.response.send_message(
                "Non è il tuo turno!", ephemeral=True
            )
            return False
        return True
class Buttons(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Buttons(bot))