import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import mysql.connector
import os

class TokenGroup(commands.GroupCog, name="token", description="comandi per impostare token o descrizione"):
    group = app_commands.Group(name="funzioni", description="funzioni di Token")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    user = os.getenv("USER")
    password = os.getenv("PASSWORD")

    db = mysql.connector.connect(
        host="eu.pylex.me",
        user=user,
        password=password,
        database="s487_Borgo_Altrove"
    )
    cursor = db.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS token (
            id VARCHAR(255) PRIMARY KEY,
            name TEXT,
            token_url TEXT,
            description TEXT
        )
    ''')

    try:
        cursor.execute("SELECT DATABASE()")
        print("Connesso al Database!")
    except mysql.connector.Error as err:
        print(f"Qualcosa è andato storto con il Database: {err}")

    #### VIEW 
    @app_commands.command()
    async def view(ctx: discord.Interaction, *, player: discord.Member = None):
        user_id = str(player.id or ctx.author.id)
        cursor.execute('SELECT token_url, description FROM token WHERE id = %s', (user_id,))
        result = cursor.fetchone()
        if result is None:
            await ctx.response.send_message(f"Mi dispiace, ma non vi è alcuna descrizione salvata per <@{user_id}>. " + ('Usa il comando `!token set` per salvare un\'immagine e una descrizione per il tuo personaggio.' if not player else ''), ephemeral=True)
        else:
            name, token_url, description = result
            embed = discord.Embed(title=f"Descrizione di {name}!",
                                description=description,
                                color=0xFFFF00)
            if token_url:
                embed.set_image(url=token_url)
            await ctx.response.send_message(embed=embed)

    #### SET
    @app_commands.command()
    async def set(ctx: discord.Interaction, name: str, description: str, *, token:discord.Attachment = None):
        user_id = str(ctx.author.id)

        embed = discord.Embed(title=f"Descrizione di {name}!",
                                description=description,
                                color=0xFFFF00)
        if token:
            token_url = token.url
            embed.set_image(url=token_url)
        
        cursor.execute('REPLACE INTO token VALUES (%s, %s, %s, %s)', (user_id, name, token_url, description))
        db.commit()
        
        await ctx.response.send_message(f"Descrizione {'e token' if token else ''} impostat{'i' if token else 'o'} correttamente per {name}!", ephemeral=True)
        await ctx.followup.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(TokenGroup(bot))