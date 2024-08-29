import discord
from discord import app_commands
from discord.ext import commands, tasks
import asyncio

class basic_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # JOIN-ROLE
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != 809055669075312691:
            return
        
        if member.bot:
            role = discord.utils.get(member.guild.roles, name="BOT")
        else:
            role = discord.utils.get(member.guild.roles, name="Disperso")
        await member.add_roles(role)
        
    # REAPETED MESSAGES (In implementazione)
    @commands.command()
    async def set_message(self, ctx, channel: discord.TextChannel, *, message: str):
        self.message_channel_id = channel.id
        self.message_content = message
        await ctx.send(f"Messaggio impostato per il canale {channel.mention}: {message}")

    @tasks.loop(weeks=1)
    async def send_message(self):
        if self.message_channel_id and self.message_content:
            channel = self.bot.get_channel(self.message_channel_id)
            if channel:
                await channel.send(self.message_content)

    @send_message.before_loop
    async def before_send_message(self):
        await self.bot.wait_until_ready()

    # AUTO REACTIONS
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id in [1214564510833319988, 1202550269057957938]:
            await message.add_reaction('✅')
            await message.add_reaction('❌')
    
    # CLEAR
    @app_commands.command(name="clear", description="Cancella più messaggi assieme")
    async def clear_app(self, ctx: discord.Interaction, amount: int):
        await ctx.response.defer(ephemeral=True)
        
        await ctx.channel.purge(limit=amount)
        await ctx.followup.send(f"{amount} Messagg{'i' if amount != 1 else 'o'} eliminat{'i' if amount != 1 else 'o'}", ephemeral=True)
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx: discord.Interaction, amount: int):
        await ctx.channel.purge(limit=amount)
        if amount == 1:
            await ctx.send(f"1 Messaggio eliminato", delete_after=3)
        else:
            await ctx.send(f"{amount} Messaggi eliminati", delete_after=3)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Mi dispiace, ma non hai i permessi per usare questo comando.", delete_after=5)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Mi dispiace, ma il bot non ha i permessi per eseguire questo comando.", delete_after=5)

    # TEST
    @commands.command()
    async def test(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send(ctx.message.content[5:])
        for attachment in ctx.message.attachments:
            await ctx.send(attachment.url)

    # SHUTDOWN
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send(content = "Spegnendo il bot...", delete_after=3)
        await asyncio.sleep(3)
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(basic_commands(bot))
