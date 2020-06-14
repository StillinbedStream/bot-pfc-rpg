from discord.ext import commands
from PFCBot.commands.converters import is_name
from PFCBot.core.engine import GameManager

class SpellsCommands(commands.Cog):
    '''
    Basic Play regroupe toutes les commandes les plus basiques : 
    - s0cattack
    - fallellyss
    '''
    def __init__(self, bot, game_manager: GameManager):
        self.bot = bot
        self.game_manager = game_manager


    @commands.command(name='s0cattack')
    @commands.dm_only()
    async def s0command(self, ctx, name_player2: str):
        await self.game_manager.use_spell('s0cattack', ctx.message.author.id, ctx.message.channel, name_player2)

    @commands.command(name="fallellyss")
    @commands.dm_only()
    async def fallelyss(self, ctx, name_player2: is_name):
        await self.game_manager.fallEllyss(ctx.message.author.id, name_player2, ctx.channel)

