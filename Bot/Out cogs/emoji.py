import discord
from discord.ext import commands
from discord import app_commands
import asyncio

import nest_asyncio
nest_asyncio.apply()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
    
emoji = app_commands.Group(name="math", description="Math commands")

### EMOJI BORGO
@emoji.command()
async def show(ctx):
    server = bot.get_guild(809055669075312691)
    embed = discord.Embed(title="Emoji del server", color=0x2f3136)
    field_count = 0
    for emoji in server.emojis:
        if field_count == 25:
            await ctx.channel.send(embed=embed)
            embed = discord.Embed(title="Emoji del server (continua)", color=0x2f3136)
            field_count = 0
        if emoji.animated:
            embed.add_field(name=f"<a:{emoji.name}:{emoji.id}> {emoji.name}", value=f"ID: {emoji.id}\nURL: {emoji.url}")
        else:
            embed.add_field(name=f"<:{emoji.name}:{emoji.id}> {emoji.name}", value=f"ID: {emoji.id}\nURL: {emoji.url}")
        field_count += 1
    
    await ctx.channel.send(embed=embed)

#### LOCK EMOJI
@bot.command()
async def lock(ctx, emoji: discord.Emoji, role: discord.Role):
    if emoji is None:
        await ctx.send("Emoji non trovato.", ephemeral=True)
        return

    if role is None:
        await ctx.send("Ruolo non trovato.", ephemeral=True)
        return
    
    bot_role = ctx.guild.get_member(bot.user.id).roles[1]
    
    try:
        await emoji.edit(roles=[role, bot_role])
        await ctx.send(f"L'emoji {emoji} è ora riservato al ruolo {role.mention}.", silent=True, delete_after=10)
    except discord.Forbidden:
        await ctx.send("Non ho i permessi per modificare questo emoji.", delete_after=10)
    except discord.HTTPException as e:
        await ctx.send(f"Si è verificato un errore durante la modifica dell'emoji: {e}", delete_after=10)

#### DELOCK EMOJI
@bot.command()
async def delock(ctx, emoji: discord.Emoji):
    if emoji is None:
        await ctx.send("Emoji non trovato.")
        return

    try:
        await emoji.edit(roles=[])
        await ctx.send(f"L'emoji {emoji} è ora disponibile per tutti i ruoli.", silent=True, delete_after=10)
    except discord.Forbidden:
        await ctx.send("Non ho i permessi per modificare questo emoji.", delete_after=5)
    except discord.HTTPException as e:
        await ctx.send(f"Si è verificato un errore durante la modifica dell'emoji: {e}", delete_after=10)

#### LOCK EMOJI TREE
# **NON FUNZIONA L'AUTOCOMPLETE**
# async def emoji_autocomplete(ctx: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
#     options = [app_commands.Choice(name=emoji.name, value=emoji.name) for emoji in ctx.guild.emojis]
#     return [app_commands.Choice(name=option, value=option) for option in options if option.lower().startswith(current.lower())][:25]

@emoji.command(description= "Rendi delle emoji utilizzabili solo a determinati ruoli")
# @app_commands.autocomplete(nome_emoji = emoji_autocomplete)
@app_commands.describe(nome_emoji="Emoji da limitare")
@app_commands.describe(ruolo="Ruolo a cui è permesso usare l'emoji")
async def lock(ctx, nome_emoji: str, ruolo: discord.Role):
    
    for emoji in ctx.guild.emojis:
        app_commands.Choice(name=emoji.name, value=emoji.name)
    
    emoji = discord.utils.get(ctx.guild.emojis, name=nome_emoji)
    
    if ruolo is None:
        await ctx.response.send_message("Ruolo non trovata.", ephemeral=True)
        return
    
    bot_role = ctx.guild.get_member(bot.user.id).roles[1]
    
    try:
        await emoji.edit(roles=[ruolo, bot_role])
        await ctx.response.send_message(f"L'emoji {emoji} è ora riservato al ruolo {ruolo.mention}.", silent=True, ephemeral=True)
    except discord.Forbidden:
        await ctx.response.send_message("Non ho i permessi per modificare questo emoji.", ephemeral=True)
    except discord.HTTPException as e:
        await ctx.response.send_message(f"Si è verificato un errore durante la modifica dell'emoji: {e}", ephemeral=True)

#### DELOCK EMOJI TREE
@emoji.command()
async def delock(ctx, nome_emoji: str):
    emoji = discord.utils.get(ctx.guild.emojis, name=nome_emoji)
    if emoji is None:
        await ctx.response.send_message("Emoji non trovata.")
        return

    try:
        await emoji.edit(roles=[])
        await ctx.response.send_message(f"L'emoji {emoji} è ora disponibile per tutti i ruoli.", silent=True, ephemeral=True)
    except discord.Forbidden:
        await ctx.response.send_message("Non ho i permessi per modificare questo emoji.", ephemeral=True)
    except discord.HTTPException as e:
        await ctx.response.send_message(f"Si è verificato un errore durante la modifica dell'emoji: {e}", ephemeral=True)