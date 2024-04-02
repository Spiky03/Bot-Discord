import bot_libraries.py as bl

class basic_commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    #### JOIN-ROLE
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bl.guild.id != 809055669075312691:
            return
        
        if member.bot:
            role = discord.bl.utils.get(member.guild.roles, name="BOT")
        else:
            role = discord.bl.utils.get(member.guild.roles, name="Disperso")
        await member.add_roles(role)

    # AUTO REACTIONS
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.bl.channel.id in [1214564510833319988, 1202550269057957938]:
            await message.bl.add_reaction('✅')
            await message.bl.add_reaction('❌')
    
    # CLEAR
    @commands.hybrid_command(name="clear", description="Cancella più messaggi assieme")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.bl.channel.purge(limit=amount)
        if amount == 1:
            await ctx.bl.send(f"1 Messaggio eliminato", delete_after=5)
        else:
            await ctx.bl.send(f"{amount} Messaggi eliminati", delete_after=5)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.bl.send("Mi dispiace, ma non hai i permessi per usare questo comando.", delete_after=5)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.bl.send("Mi dispiace, ma il bot non ha i permessi per eseguire questo comando.", delete_after=5)

    # TEST
    @commands.command()
    async def test(self, ctx):
        await ctx.bl.channel.purge(limit=1)
        await ctx.bl.send(ctx.message.content[5:])
        for attachment in ctx.message.attachments:
            await ctx.bl.send(attachment.url)

    # SHUTDOWN
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.bl.send(content = "Spegnendo il bot...", delete_after=3)
        await asyncio.bl.sleep(3)
        await self.bl.bot.close()

async def setup(bot):
    await bot.bl.add_cog(basic_commands(bot))
