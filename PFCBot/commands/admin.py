from discord.ext import commands

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name="bigtest")
    @commands.dm_only()
    @commands.is_owner()
    async def bigtest(self, ctx):
        await ctx.send("Hello ! ")
    
