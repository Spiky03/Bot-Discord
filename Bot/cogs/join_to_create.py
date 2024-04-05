import discord
from discord.ext import commands
import asyncio
import random

class JTCC(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        # SALE MASTER
        if after.channel and after.channel.name == '🔉・Sale Master':
            if discord.utils.get(member.roles, name='Master'):
                
                # Funzione per trovare la sala
                def trova_sala(id):
                    name_sala = {
                        '🌮・Sala Tacos': [507830047005081602],
                        '🎡・Sala Lunapark': [1074415066591543436, 329979827580960780, 172074260863385600],
                        '⚰️・Sala Bara': [685409172040319026, 433227911865303040, 474762084677320704, 569976596321009674],
                        '🪅・Sala Pignatta': [687754586462748747],
                        '🥑・Sala Avocado': [],
                        '☕・Sala Caffè': [316981699571613697],
                        '🥟・Sala Tortellino': [686199276765839373, 326706374337888256],
                        '🍷・Sala Vino': [303927342970044416, 708039190352232558, 223190037691498496],
                        '🏕・Sala Campeggio': [688092486584762477, 273246007066624001],
                        '🦄・Sala Unicorno': [463687872088768522, 393891222781034499, 276762790201524224]
                                 }
                    for sala, ids in name_sala.items():
                        if id in ids:
                            return sala
                    return f'🔉Sala Master {sum(1 for i in category.channels if "Sala Master" in i.name)+1}'
                
                category = after.channel.category
                new_channel = await category.create_voice_channel(trova_sala(member.id))
                await member.move_to(new_channel)

            else:
                await member.send('Mi disipiace ma non sei un **Master di [Borgo Altrove](<https://discord.gg/borgo-altrove-809055669075312691>)**. Attendi prima che un Master crei una sala per la vostra sessione!')

        # SALE SPAM
        elif after.channel and after.channel.name == '❮💩❯・Sale Spam':
            category = after.channel.category
            # easter egg
            if random.randint(1, 1000000) == 1:
                new_channel = await category.create_voice_channel('❮🍺❯・𝑻𝒂𝒗𝒆𝒓𝒏𝒂')
                await new_channel.send(f"Che fortuna {member.mention}! Avevi **1 possibilità su un milione** di creare questo antico canale!")
            else:
                new_channel = await category.create_voice_channel(f'❮💩❯・Sala Spam {sum(1 for i in category.channels if "Sala Spam" in i.name)+1}')
            await member.move_to(new_channel)

        # SALE REGIONALI
        name_sala_regionale = {
            'Laziese':'Sala Lupacchiotti', 'Siciliano':'Sala Arancino', 'Sardo':'Sala cappitto mi hai', 'Pugliese':'Sala Panzerotto',
             'Lucano':'Sala Pecorari', 'Calabrese':'Sala Scimmie', 'Campano':'Sala Pickpocket', 'Abbruzzese':'Sala Terremotati', 'Liguri':'Sala Pota',
             'Umbro':'Sala Cinghiale', 'Toscano':'Sala Maremma Maiala', 'Emiliano-Romagnolo':'Sala Fascisti', 'Piemontese':'Sala Minchia Diofa',
             'Lombrado':'Sala Aperitivo', 'Veneto':'Sala Bestemmiatori', 'Friuliano':'Sala Tristini', 'Marchigiano':'Sala Porcamadoro',
             'Trentino':'Sala Ammazza Orsi'
             }
        
        if after.channel and after.channel.name == '🔉・Sale Regionali':
            category = after.channel.category
            if member.roles[1].name in name_sala_regionale.keys():
                new_channel = await category.create_voice_channel(f'🔉・{name_sala_regionale[member.roles[1].name]}')
            else:
                new_channel = await category.create_voice_channel(f'🔉・Sala Regionale {sum(1 for i in category.channels if "Sala Regionale" in i.name)+1}')
            await member.move_to(new_channel)

        # ELIMINA SALE
        if before.channel and ('Sala' in before.channel.name or '𝑻𝒂𝒗𝒆𝒓𝒏𝒂' in before.channel.name):
            async def delete_channel_if_empty(channel):
                await asyncio.sleep(1)  # aspetta per 1 secondo
                if not channel.members:
                    await channel.delete()
            asyncio.create_task(delete_channel_if_empty(before.channel))

async def setup(bot):
    await bot.add_cog(JTCC(bot))