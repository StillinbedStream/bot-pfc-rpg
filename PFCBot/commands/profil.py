from discord.ext import commands
from PFCBot.commands.converters import is_name
from PFCBot.core.engine import GameManager

class ProfilCommands(commands.Cog):
    '''
    Profil commands like : 
    - mysignature
    - signature
    '''
    def __init__(self, bot, game_manager: GameManager):
        self.bot = bot
        self.game_manager = game_manager

        

    @commands.command(name='signature')
    @commands.dm_only()
    async def signature(self, ctx, signature: str, signature_image: str = ""):
        await self.game_manager.signature(ctx.message.author.id, signature, signature_image, ctx.channel)


    @commands.command(name='mysignature')
    @commands.dm_only()
    async def mysignature(self, ctx):
        await self.game_manager.mysignature(ctx.message.author.id, ctx.channel)


    @commands.command(name="mobile")
    @commands.dm_only()
    async def mobile(self, ctx):
        await self.game_manager.mobile(ctx.message.author.id, ctx.channel)
        
