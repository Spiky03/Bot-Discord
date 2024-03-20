import config
from sessione import proposta_sessione_tree #, proposta_sessione
from join_to_create import join_to_create_channel

import discord
from discord.ext import commands
import asyncio

from colorama import just_fix_windows_console
from colorama import Fore #, Back, Style
just_fix_windows_console()

import nest_asyncio
nest_asyncio.apply()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

#### PROSPOSTA SESSIONE & TRANSIZIONE
@bot.tree.command(name="sessione", description="Proponi una tua Sessione ai responsabili Trama & Lore!")
async def sessione(ctx):
    await proposta_sessione_tree(ctx, bot)

#### JOIN-TO-CERATE-CHANNEL
@bot.event
async def on_voice_state_update(member, before, after):
    await join_to_create_channel(member, before, after, bot)

#### CLEAR
@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.response.send(f"{amount} Messaggi{'o' if amount == 1 else ''} eliminat{'o' if amount == 1 else 'i'}", ephemeral=True)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.response.send("Mi dispiace, ma non hai i permessi per usare questo comando.", ephemeral=True)
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.response.send("Mi dispiace, ma il bot non ha i permessi per eseguire questo comando.", ephemeral=True)

#### TEST
@bot.command()
async def test(ctx, arg: str):
    await ctx.send(arg)

#### JOIN-ROLE
@bot.event
async def on_member_join(member):
    if member.guild.id != 809055669075312691:
        return
    
    if member.bot:
        role = discord.utils.get(member.guild.roles, name="BOT")
    else:
        role = discord.utils.get(member.guild.roles, name="Disperso")
    await member.add_roles(role)

##### SHUTDOWN
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send(content = "Spegnendo il bot...", delete_after=3)
    await asyncio.sleep(3)
    await bot.close()

#### READY
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(Fore.CYAN + 'Connesso a ' + str(len(synced)) + ' comando/i')
    except Exception as e:
        print(e)
    
    print(f'Bot pronto e carico all\'uso come {bot.user}\n----------------------------------------------------'+ Fore.RED)
    
bot.run(config.DISCORD_TOKEN)
