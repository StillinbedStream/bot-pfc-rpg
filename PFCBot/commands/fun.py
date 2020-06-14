from discord.ext import commands

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="leplusbeau")
    @commands.dm_only()
    async def leplusbeau(self, ctx):
        '''
            Cette commande a été mise en place pour le stream caritatif de 
            l'AUEC pour un hôpital. 
        '''
        await ctx.send("Le plus beau c'est <@289061712043442176>")
