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
        view: KnucklebonesView = self.view
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
        view: KnucklebonesView = self.view
        p1 = view.p1
        p2 = view.p2
        channel = view.channel
        
        timeout = 300.0
        
        view = KnucklebonesView(p1, p2, channel, timeout=timeout)
        view.add_item(tiraButton("p2"))
        view.add_item(resaButton())

        embed = discord.Embed(
            title=f"{p2.display_name} è il tuo turno!", 
            description="Scegli cosa fare!",
            color=discord.Color.dark_red()
        )
        embed.set_author(
            name=p2.display_name,
            icon_url=p2.avatar.url
        )
        
        msg = await channel.send(embeds=griglie(p1, p2, view.griglia1, view.griglia2, view.pt1, view.pt2) + [embed], view=view)

        embed = discord.Embed(title="Hai accettato la sfida a **Knucklebones**", description=f"[Vai alla sfida!](<{msg.jump_url}>)")
        await ctx.response.send_message(embed=embed, ephemeral=True)

class tiraButton(Button):
    def __init__(self, p):
        super().__init__(label="Tira!", style=discord.ButtonStyle.blurple)
        self.p = p
        
    async def callback(self, ctx: discord.Interaction):
        view: View = self.view
        player = view.p1 if self.p == "p1" else view.p2
        if ctx.user != player:
            await ctx.response.send_message("Non è il tuo turno!", ephemeral=True)
            return

        rolled_number = randint(1, 6)
        embed = discord.Embed(
            title=f"{player.display_name} ha tirato un {rolled_number}!",
            description="Scegli in quale colonna inserire il valore.",
            color=discord.Color.dark_red() if player == "p2" else discord.Color.dark_blue()
        )
        embed.set_author(
            name=player.display_name,
            icon_url=player.avatar.url
        )
        
        # Aggiunta dei bottoni per la scelta della colonna
        view.clear_items()
        view.add_item(ColumnButton("Sx", rolled_number, self.p))
        view.add_item(ColumnButton("Center", rolled_number, self.p))
        view.add_item(ColumnButton("Dx", rolled_number, self.p))
        view.add_item(resaButton())

        await ctx.response.edit_message(embeds=griglie(view.p1, view.p2, view.griglia1, view.griglia2, view.pt1, view.pt2) + [embed], view=view)

class ColumnButton(Button):
    def __init__(self, label, rolled_number, p):
        super().__init__(label=label, style=discord.ButtonStyle.primary)
        self.rolled_number = rolled_number
        self.p = p
        
    async def callback(self, ctx: discord.Interaction):
        view: View = self.view
        player = view.p1 if self.p == "p1" else view.p2
        if ctx.user != player:
            await ctx.response.send_message("Non è il tuo turno!", ephemeral=True)
            return

        # Logica per inserire il valore nella griglia
        col = {"Sx": 0, "Center": 1, "Dx": 2}[self.label]

        opponent_grid = view.griglia1 if self.p == "p2" else view.griglia2
        # Trova la prima cella vuota nella colonna partendo dall'alto per p2 e dal basso per p1
        if self.p == "p2":  
            for row in view.griglia2:
                if row[col] == 0:
                    row[col] = self.rolled_number
                    break
                    
            # Rimuove i numeri uguali dalla colonna dell'avversario e fa scalare i numeri
            for i in range(3):
                if opponent_grid[i][col] == self.rolled_number:
                    opponent_grid[i][col] = 0
            
            # Scala i numeri dall'alto verso il basso per p2
            for i in range(2, 0, -1):
                if opponent_grid[i][col] == 0:
                    # Trova la prima cella sopra non vuota
                    for j in range(i - 1, -1, -1):
                        if opponent_grid[j][col] != 0:
                            opponent_grid[i][col], opponent_grid[j][col] = opponent_grid[j][col], 0
                            break     
        
        else:
            for i in range(2, -1, -1):
                if view.griglia1[i][col] == 0:
                    view.griglia1[i][col] = self.rolled_number
                    break
            
            # Rimuove i numeri uguali dalla colonna dell'avversario e fa scalare i numeri
            for i in range(3):
                if opponent_grid[i][col] == self.rolled_number:
                    opponent_grid[i][col] = 0
            
            # Scala i numeri dal basso verso l'alto per p1
            for i in range(2):
                if opponent_grid[i][col] == 0:
                    # Trova la prima cella sopra non vuota
                    for j in range(2, i, -1):
                        if opponent_grid[j][col] != 0:
                            opponent_grid[i][col], opponent_grid[j][col] = opponent_grid[j][col], 0
                            break
        
       # Aggiorna il punteggio per p1
        view.pt1 = 0
        for c in range(3):
            col_vals = [view.griglia1[r][c] for r in range(3)]
            for val in set(col_vals):
                if val != 0:
                    count = col_vals.count(val)
                    # Calcola il punteggio secondo la tabella di moltiplicazione
                    if count == 1:
                        view.pt1 += val
                    elif count == 2:
                        view.pt1 += val * 4
                    elif count == 3:
                        view.pt1 += val * 9
                        
        # Aggiorna il punteggio per p1              
        view.pt2 = 0
        for c in range(3):
            col_vals = [view.griglia2[r][c] for r in range(3)]
            for val in set(col_vals):
                if val != 0:
                    count = col_vals.count(val)
                    # Calcola il punteggio secondo la tabella di moltiplicazione
                    if count == 1:
                        view.pt2 += val
                    elif count == 2:
                        view.pt2 += val * 4
                    elif count == 3:
                        view.pt2 += val * 9


        # Ripristina i bottoni per il prossimo giocatore
        next_player = view.p1 if view.turn == "p1" else view.p2
        view.clear_items()
        view.add_item(tiraButton(view.turn))
        view.add_item(resaButton())

        # Aggiorna l'embed per mostrare la nuova situazione del gioco
        embed = discord.Embed(
            title=f"{next_player.display_name} è il tuo turno!", 
            description="Scegli cosa fare!",
            color=discord.Color.dark_red() if next_player == view.p2 else discord.Color.dark_blue()
        )
        embed.set_author(
            name=next_player.display_name,
            icon_url=next_player.avatar.url
        )
        await ctx.response.edit_message(embeds=griglie(view.p1, view.p2, view.griglia1, view.griglia2, view.pt1, view.pt2) + [embed], view=view)

class KnucklebonesView(View):
    def __init__(self, p1, p2, channel, timeout=300.0):
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
            await self.message.edit(content=f"_Mi dispiace, la partita è scaduta a causa dell'inattività._", embed=None, view=None)
                            
class Buttons(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Buttons(bot))