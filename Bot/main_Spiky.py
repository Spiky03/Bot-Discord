import discord
from discord.ext import commands
from discord import app_commands
import asyncio

import os
from dotenv import load_dotenv
load_dotenv()

# TOKEN
TOKEN = os.getenv("PROVA")

# PREFIX AND INTENTS
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='^', intents=intents)

@bot.command(name="sync")
async def sync(ctx):
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s).")
    
# READY
@bot.event  
async def on_ready():
    
    # COGS
    for file in os.listdir(r"C:\Users\gagli\Documents\Bot-Discord\Bot\cogs_Spiky"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs_Spiky.{file[:-3]}")

    try:
        synced = await bot.tree.sync()
        print('Connesso a ' + str(len(synced)) + ' comando/i')
    except Exception as e:
        print(e)
    
    print(f'Bot di PROVA pronto come {bot.user}\n----------------------------------------------------')
    
bot.run(TOKEN)