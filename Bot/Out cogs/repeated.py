import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio

class Repeater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counter = 0
        self.max_repeats = 60
        self.repeater_task = None

    @app_commands.command(name="ripetizione", description="Imposta un messagggio da inviare ripetutamente")
    async def set_repeater(self, ctx: discord.Interaction, channel_id: str, interval: int, *, message: str):
        await ctx.response.defer()
        self.channel = self.bot.get_channel(int(channel_id))
        if self.channel is None:
            await ctx.followup.send("Canale non trovato. Assicurati che l'ID del canale sia corretto.")
            return
        
        self.message = message
        self.interval = interval
        self.counter = 0

        if self.repeater_task:
            self.repeater_task.cancel()

        self.repeater_task = self.repeater.start()
        await ctx.followup.send(f'Ripetizione impostata per il canale {self.channel.mention} per ogni {self.interval} second{"o" if self.interval == 1 else "i"}.')
        
    @app_commands.command(name="stop", description="Ferma la ripetizione del messaggio.")
    async def stop_repeater(self, ctx: discord.Interaction):
        await ctx.response.defer()
        if self.repeater_task:
            self.repeater_task.cancel()
            self.repeater_task = None
            await ctx.followup.send("Ripetizione fermata.")
        else:
            await ctx.followup.send("Non vi è alcuna ripetizione al momento.")
            
    @tasks.loop(seconds=1)
    async def repeater(self):
        if self.counter < self.max_repeats:
            await self.channel.send(self.message)
            self.counter += 1
            await asyncio.sleep(self.interval)
        else:
            self.repeater_task.cancel()
            
async def setup(bot):
    await bot.add_cog(Repeater(bot))





